import gc
import json
import random
from pathlib import Path
from time import time

from exllamav2 import (
    ExLlamaV2,
    ExLlamaV2Cache,
    ExLlamaV2Cache_Q4,
    ExLlamaV2Cache_Q6,
    ExLlamaV2Cache_Q8,
    ExLlamaV2Config,
    ExLlamaV2Tokenizer,
)
from exllamav2.generator import (
    ExLlamaV2DynamicGenerator,
    ExLlamaV2DynamicJob,
    ExLlamaV2Sampler,
)
from jinja2 import Template

from comfy.model_management import soft_empty_cache, unload_all_models
from comfy.utils import ProgressBar
from folder_paths import add_model_folder_path, get_folder_paths, models_dir

_CATEGORY = "Zuellni/ExLlama"
_MAPPING = "ZuellniExLlama"


class Loader:
    @classmethod
    def INPUT_TYPES(cls):
        add_model_folder_path("llm", str(Path(models_dir) / "llm"))

        for folder in get_folder_paths("llm"):
            for path in Path(folder).rglob("*/"):
                if (path / "config.json").is_file():
                    parent = path.relative_to(folder).parent
                    cls._MODELS[str(parent / path.name)] = path

        models = list(cls._MODELS.keys())
        caches = list(cls._CACHES.keys())
        default = models[0] if models else None

        return {
            "required": {
                "model": (models, {"default": default}),
                "cache_bits": (caches, {"default": 4}),
                "fast_tensors": ("BOOLEAN", {"default": True}),
                "flash_attention": ("BOOLEAN", {"default": True}),
                "max_seq_len": ("INT", {"default": 2048, "max": 2**20, "step": 256}),
            }
        }

    _CACHES = {
        4: lambda m: ExLlamaV2Cache_Q4(m, lazy=True),
        6: lambda m: ExLlamaV2Cache_Q6(m, lazy=True),
        8: lambda m: ExLlamaV2Cache_Q8(m, lazy=True),
        16: lambda m: ExLlamaV2Cache(m, lazy=True),
    }
    _MODELS = {}
    CATEGORY = _CATEGORY
    FUNCTION = "setup"
    RETURN_NAMES = ("MODEL",)
    RETURN_TYPES = ("EXL_MODEL",)

    def setup(self, model, cache_bits, fast_tensors, flash_attention, max_seq_len):
        self.unload()
        self.cache_bits = cache_bits

        self.config = ExLlamaV2Config(__class__._MODELS[model])
        self.config.fasttensors = fast_tensors
        self.config.no_flash_attn = not flash_attention

        if max_seq_len:
            self.config.max_seq_len = max_seq_len

            if self.config.max_input_len > max_seq_len:
                self.config.max_input_len = max_seq_len
                self.config.max_attention_size = max_seq_len**2

        self.tokenizer = ExLlamaV2Tokenizer(self.config)
        return (self,)

    def load(self):
        if (
            hasattr(self, "model")
            and hasattr(self, "cache")
            and hasattr(self, "generator")
            and self.model
            and self.cache
            and self.generator
        ):
            return

        self.model = ExLlamaV2(self.config)
        self.cache = __class__._CACHES[self.cache_bits](self.model)

        progress = ProgressBar(len(self.model.modules))
        self.model.load_autosplit(self.cache, callback=lambda _, __: progress.update(1))

        self.generator = ExLlamaV2DynamicGenerator(
            model=self.model,
            cache=self.cache,
            tokenizer=self.tokenizer,
            paged=not self.config.no_flash_attn,
        )

    def unload(self):
        if hasattr(self, "model") and self.model:
            self.model.unload()

        self.model = None
        self.cache = None
        self.generator = None

        gc.collect()
        soft_empty_cache()


class Formatter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("EXL_MODEL",),
                "messages": ("EXL_MESSAGES",),
                "add_assistant_role": ("BOOLEAN", {"default": True}),
            }
        }

    CATEGORY = _CATEGORY
    FUNCTION = "format"
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def raise_exception(self, message):
        raise Exception(message)

    def render(self, template, messages, add_assistant_role):
        return (
            template.render(
                add_generation_prompt=add_assistant_role,
                raise_exception=self.raise_exception,
                messages=messages,
                bos_token="",
            ),
        )

    def format(self, model, messages, add_assistant_role):
        template = model.tokenizer.tokenizer_config_dict["chat_template"]
        template = Template(template)

        try:
            return self.render(template, messages, add_assistant_role)
        except:
            system = None
            merged = []

            for message in messages:
                if message["role"] == "system":
                    system = {"role": "user", "content": message["content"]}
                    merged.append(system)
                elif system and message["role"] == "user":
                    index = merged.index(system)
                    merged[index]["content"] += "\n" + message["content"]
                    system = None
                else:
                    merged.append(message)
                    system = None

            return self.render(template, merged, add_assistant_role)


class Tokenizer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("EXL_MODEL",),
                "text": ("STRING", {"forceInput": True}),
                "add_bos_token": ("BOOLEAN", {"default": True}),
                "encode_special_tokens": ("BOOLEAN", {"default": True}),
            }
        }

    CATEGORY = _CATEGORY
    FUNCTION = "tokenize"
    RETURN_NAMES = ("TOKENS",)
    RETURN_TYPES = ("EXL_TOKENS",)

    def tokenize(self, model, text, add_bos_token, encode_special_tokens):
        return (
            model.tokenizer.encode(
                text=text,
                add_bos=add_bos_token,
                encode_special_tokens=encode_special_tokens,
            ),
        )


class Settings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "temperature": ("FLOAT", {"default": 1, "max": 10, "step": 0.01}),
                "penalty": ("FLOAT", {"default": 1, "min": 1, "max": 10, "step": 0.01}),
                "top_k": ("INT", {"default": 1, "max": 1000}),
                "top_p": ("FLOAT", {"max": 1, "step": 0.01}),
                "top_a": ("FLOAT", {"max": 1, "step": 0.01}),
                "min_p": ("FLOAT", {"max": 1, "step": 0.01}),
                "tfs": ("FLOAT", {"max": 1, "step": 0.01}),
                "typical": ("FLOAT", {"max": 1, "step": 0.01}),
                "temperature_last": ("BOOLEAN", {"default": True}),
            }
        }

    CATEGORY = _CATEGORY
    FUNCTION = "set"
    RETURN_NAMES = ("SETTINGS",)
    RETURN_TYPES = ("EXL_SETTINGS",)

    def set(
        self,
        temperature,
        penalty,
        top_k,
        top_p,
        top_a,
        min_p,
        tfs,
        typical,
        temperature_last,
    ):
        settings = ExLlamaV2Sampler.Settings()
        settings.temperature = temperature
        settings.token_repetition_penalty = penalty
        settings.top_k = top_k
        settings.top_p = top_p
        settings.top_a = top_a
        settings.min_p = min_p
        settings.tfs = tfs
        settings.typical = typical
        settings.temperature_last = temperature_last
        return (settings,)


class Generator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("EXL_MODEL",),
                "tokens": ("EXL_TOKENS",),
                "unload": ("BOOLEAN", {"default": False}),
                "stop_conditions": ("STRING", {"default": r'"\n"'}),
                "max_tokens": ("INT", {"default": 128, "max": 2**20}),
                "seed": ("INT", {"max": 2**64 - 1}),
            },
            "optional": {"settings": ("EXL_SETTINGS",)},
        }

    CATEGORY = _CATEGORY
    FUNCTION = "generate"
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def generate(
        self,
        model,
        tokens,
        unload,
        stop_conditions,
        max_tokens,
        seed,
        settings=None,
    ):
        if unload:
            unload_all_models()
            model.unload()

        model.load()
        random.seed(seed)
        tokens_len = tokens.shape[-1]
        max_len = model.config.max_seq_len - tokens_len
        stop = [model.tokenizer.eos_token_id]

        if not max_tokens or max_tokens > max_len:
            max_tokens = max_len

        if stop_conditions.strip():
            stop_conditions = json.loads(f"[{stop_conditions}]")
            stop.extend(stop_conditions)

        if not settings:
            settings = ExLlamaV2Sampler.Settings()
            settings.greedy()

        job = ExLlamaV2DynamicJob(
            input_ids=tokens,
            max_new_tokens=max_tokens,
            stop_conditions=stop,
            gen_settings=settings,
        )

        progress = ProgressBar(max_tokens)
        model.generator.enqueue(job)
        start = time()
        eos = False
        chunks = []
        count = 0

        while not eos:
            for response in model.generator.iterate():
                if response["stage"] == "streaming":
                    chunk = response.get("text", "")
                    eos = response["eos"]
                    chunks.append(chunk)
                    progress.update(1)
                    count += 1

        output = "".join(chunks)
        total = round(time() - start, 2)
        speed = round(count / total, 2)

        print(
            f"Output generated in {total} seconds",
            f"({tokens_len} context, {count} tokens, {speed}t/s)",
        )

        if unload:
            model.unload()

        return (output,)


NODE_CLASS_MAPPINGS = {
    f"{_MAPPING}Loader": Loader,
    f"{_MAPPING}Formatter": Formatter,
    f"{_MAPPING}Tokenizer": Tokenizer,
    f"{_MAPPING}Settings": Settings,
    f"{_MAPPING}Generator": Generator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    f"{_MAPPING}Loader": "Loader",
    f"{_MAPPING}Formatter": "Formatter",
    f"{_MAPPING}Tokenizer": "Tokenizer",
    f"{_MAPPING}Settings": "Settings",
    f"{_MAPPING}Generator": "Generator",
}
