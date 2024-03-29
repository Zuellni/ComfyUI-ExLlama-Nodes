import gc
import random
from pathlib import Path
from time import time

import torch
from comfy.model_management import soft_empty_cache, unload_all_models
from comfy.utils import ProgressBar
from exllamav2 import (
    ExLlamaV2,
    ExLlamaV2Cache,
    ExLlamaV2Cache_8bit,
    ExLlamaV2Config,
    ExLlamaV2Tokenizer,
)
from exllamav2.generator import ExLlamaV2Sampler, ExLlamaV2StreamingGenerator
from folder_paths import add_model_folder_path, get_folder_paths, models_dir


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
                "gpu_split": ("STRING", {"default": ""}),
                "cache_8bit": ("BOOLEAN", {"default": False}),
                "max_seq_len": ("INT", {"default": 1024, "max": 2**16}),
            },
        }

    _MODELS = {}
    CATEGORY = "Zuellni/ExLlama"
    FUNCTION = "setup"
    RETURN_NAMES = ("MODEL",)
    RETURN_TYPES = ("EXL_MODEL",)

    def setup(self, model, gpu_split, cache_8bit, max_seq_len):
        self.unload()
        self.config = ExLlamaV2Config()
        self.config.model_dir = __class__._MODELS[model]
        self.config.prepare()

        if max_seq_len:
            self.config.max_seq_len = max_seq_len

        self.gpu_split = [float(a) for a in gpu_split.split(",") if gpu_split]
        self.cache_8bit = cache_8bit

        return (self,)

    def load(self):
        if (
            hasattr(self, "model") and
            hasattr(self, "cache") and
            hasattr(self, "tokenizer") and
            hasattr(self, "generator") and
            self.model and
            self.cache and
            self.tokenizer and
            self.generator
        ):
            return

        self.model = ExLlamaV2(self.config)
        progress = ProgressBar(len(self.model.modules))

        self.model.load(
            gpu_split=self.gpu_split,
            callback=lambda s, _: progress.update_absolute(s),
        )

        self.cache = (
            ExLlamaV2Cache_8bit(self.model)
            if self.cache_8bit
            else ExLlamaV2Cache(self.model)
        )

        self.tokenizer = ExLlamaV2Tokenizer(self.config)

        self.generator = ExLlamaV2StreamingGenerator(
            model=self.model,
            cache=self.cache,
            tokenizer=self.tokenizer,
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
                "single_line": ("BOOLEAN", {"default": False}),
                "max_tokens": ("INT", {"default": 128, "max": 2**16}),
                "temperature": ("FLOAT", {"default": 1, "max": 5, "step": 0.01}),
                "top_k": ("INT", {"max": 200}),
                "top_p": ("FLOAT", {"default": 1, "max": 1, "step": 0.01}),
                "typical_p": ("FLOAT", {"default": 1, "max": 1, "step": 0.01}),
                "min_p": ("FLOAT", {"max": 1, "step": 0.01}),
                "top_a": ("FLOAT", {"max": 1, "step": 0.01}),
                "penalty": ("FLOAT", {"default": 1, "min": 1, "max": 3, "step": 0.01}),
                "temperature_last": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"max": 2**64 - 1}),
                "text": ("STRING", {"multiline": True}),
            },
            "hidden": {
                "info": "EXTRA_PNGINFO",
                "id": "UNIQUE_ID",
            },
        }

    CATEGORY = "Zuellni/ExLlama"
    FUNCTION = "generate"
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def generate(
        self,
        model,
        unload,
        single_line,
        max_tokens,
        temperature,
        top_k,
        top_p,
        typical_p,
        min_p,
        top_a,
        penalty,
        temperature_last,
        seed,
        text,
        info=None,
        id=None,
    ):
        if not text:
            return ("",)

        if unload:
            unload_all_models()
            model.unload()

        model.load()
        input = model.tokenizer.encode(text, encode_special_tokens=True)
        input_len = input.shape[-1]
        max_len = model.config.max_seq_len - input_len
        stop = [model.tokenizer.eos_token_id]

        if not max_tokens or max_tokens > max_len:
            max_tokens = max_len

        if single_line:
            stop.append(model.tokenizer.newline_token_id)

        model.generator.set_stop_conditions(stop)
        random.seed(seed)

        settings = ExLlamaV2Sampler.Settings()
        settings.temperature = temperature
        settings.top_k = top_k
        settings.top_p = top_p
        settings.typical = typical_p
        settings.min_p = min_p
        settings.top_a = top_a
        settings.token_repetition_penalty = penalty
        settings.temperature_last = temperature_last

        start = time()
        model.generator.begin_stream(input, settings)
        progress = ProgressBar(max_tokens)
        eos = False
        output = ""
        tokens = 0

        while not eos and tokens < max_tokens:
            chunk, eos, _ = model.generator.stream()
            progress.update(1)
            output += chunk
            tokens += 1

        output = output.strip()
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
    "ZuellniExLlamaLoader": Loader,
    "ZuellniExLlamaGenerator": Generator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZuellniExLlamaLoader": "Loader",
    "ZuellniExLlamaGenerator": "Generator",
}
