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
        default = models[0] if models else None

        return {
            "required": {
                "model": (models, {"default": default}),
                "cache_bits": ((4, 6, 8, 16), {"default": 16}),
                "fast_tensors": ("BOOLEAN", {"default": True}),
                "flash_attention": ("BOOLEAN", {"default": True}),
                "max_seq_len": ("INT", {"default": 2048, "max": 2**20}),
            },
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
                self.config.max_attention_len = max_seq_len**2

        return (self,)

    def load(self):
        if (
            hasattr(self, "model")
            and hasattr(self, "cache")
            and hasattr(self, "tokenizer")
            and hasattr(self, "generator")
            and self.model
            and self.cache
            and self.tokenizer
            and self.generator
        ):
            return

        self.model = ExLlamaV2(self.config)
        progress = ProgressBar(len(self.model.modules) + 1)

        self.cache = (
            ExLlamaV2Cache_Q4(self.model, lazy=True)
            if self.cache_bits == 4
            else ExLlamaV2Cache_Q6(self.model, lazy=True)
            if self.cache_bits == 6
            else ExLlamaV2Cache_Q8(self.model, lazy=True)
            if self.cache_bits == 8
            else ExLlamaV2Cache(self.model, lazy=True)
        )

        self.tokenizer = ExLlamaV2Tokenizer(self.config)
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
        self.tokenizer = None
        self.generator = None

        gc.collect()
        soft_empty_cache()


class Generator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("EXL_MODEL",),
                "unload": ("BOOLEAN", {"default": False}),
                "stop_conditions": ("STRING", {"default": r'["\n"]'}),
                "max_tokens": ("INT", {"default": 128, "max": 2**20}),
                "temperature": ("FLOAT", {"default": 1, "max": 5, "step": 0.01}),
                "top_k": ("INT", {"max": 200}),
                "top_p": ("FLOAT", {"default": 1, "max": 1, "step": 0.01}),
                "typical_p": ("FLOAT", {"default": 1, "max": 1, "step": 0.01}),
                "min_p": ("FLOAT", {"max": 1, "step": 0.01}),
                "top_a": ("FLOAT", {"max": 1, "step": 0.01}),
                "repetition_penalty": ("FLOAT", {"default": 1, "min": 1, "max": 3, "step": 0.01}),
                "temperature_last": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"max": 2**64 - 1}),
                "text": ("STRING", {"multiline": True}),
            },
            "hidden": {
                "info": "EXTRA_PNGINFO",
                "id": "UNIQUE_ID",
            },
        }

    CATEGORY = _CATEGORY
    FUNCTION = "generate"
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def generate(
        self,
        model,
        unload,
        stop_conditions,
        max_tokens,
        temperature,
        top_k,
        top_p,
        typical_p,
        min_p,
        top_a,
        repetition_penalty,
        temperature_last,
        seed,
        text,
        info=None,
        id=None,
    ):
        if not text.strip():
            return ("",)

        if unload:
            unload_all_models()
            model.unload()

        model.load()
        random.seed(seed)
        input = model.tokenizer.encode(text, encode_special_tokens=True)
        input_len = input.shape[-1]
        max_len = model.config.max_seq_len - input_len
        stop = [model.tokenizer.eos_token_id]

        if not max_tokens or max_tokens > max_len:
            max_tokens = max_len

        if stop_conditions.strip():
            stop_conditions = json.loads(stop_conditions)
            stop.extend(stop_conditions)

        settings = ExLlamaV2Sampler.Settings()
        settings.temperature = temperature
        settings.top_k = top_k
        settings.top_p = top_p
        settings.typical = typical_p
        settings.min_p = min_p
        settings.top_a = top_a
        settings.token_repetition_penalty = repetition_penalty
        settings.temperature_last = temperature_last

        job = ExLlamaV2DynamicJob(
            input_ids=input,
            max_new_tokens=max_tokens,
            stop_conditions=stop,
        )

        progress = ProgressBar(max_tokens)
        model.generator.enqueue(job)
        start = time()
        eos = False
        chunks = []
        tokens = 0

        while not eos:
            for response in model.generator.iterate():
                if response["stage"] == "streaming":
                    chunk = response.get("text", "")
                    eos = response["eos"]
                    chunks.append(chunk)
                    progress.update(1)
                    tokens += 1

        output = "".join(chunks).strip()
        total = round(time() - start, 2)
        speed = round(tokens / total, 2)

        print(
            f"Output generated in {total} seconds",
            f"({input_len} context, {tokens} tokens, {speed}t/s)",
        )

        if unload:
            model.unload()

        if id and info and "workflow" in info:
            nodes = info["workflow"]["nodes"]
            node = next((n for n in nodes if str(n["id"]) == id), None)

            if node:
                node["widgets_values"] = [output]

        return (output,)


NODE_CLASS_MAPPINGS = {
    f"{_MAPPING}Loader": Loader,
    f"{_MAPPING}Generator": Generator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    f"{_MAPPING}Loader": "Loader",
    f"{_MAPPING}Generator": "Generator",
}
