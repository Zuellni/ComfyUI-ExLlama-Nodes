import gc
import random
from time import time

import torch
from comfy.model_management import soft_empty_cache
from comfy.utils import ProgressBar
from exllamav2 import ExLlamaV2, ExLlamaV2Cache, ExLlamaV2Cache_8bit, ExLlamaV2Config, ExLlamaV2Tokenizer
from exllamav2.generator import ExLlamaV2Sampler, ExLlamaV2StreamingGenerator


class Loader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_dir": ("STRING", {"default": ""}),
                "gpu_split": ("STRING", {"default": ""}),
                "cache_8bit": ("BOOLEAN", {"default": False}),
                "max_seq_len": ("INT", {"default": 1024, "max": 2**16}),
            },
        }

    CATEGORY = "Zuellni/ExLlama"
    FUNCTION = "process"
    RETURN_NAMES = ("MODEL",)
    RETURN_TYPES = ("EXL_MODEL",)

    def __init__(self):
        self.config = None
        self.base = None
        self.cache = None
        self.tokenizer = None
        self.generator = None
        self.gpu_split = None
        self.cache_8bit = False
        self.cache_lazy = False

    def process(self, model_dir, gpu_split, cache_8bit, max_seq_len):
        self.unload()
        self.config = ExLlamaV2Config()
        self.config.model_dir = model_dir
        self.config.prepare()

        if gpu_split == "auto":
            self.cache_lazy = True
        elif gpu_split:
            self.gpu_split = [float(a) for a in gpu_split.split(",")]

        if max_seq_len:
            self.config.max_seq_len = max_seq_len

        self.cache_8bit = cache_8bit
        self.load()

        return (self,)

    def load(self):
        if self.base:
            return

        self.base = ExLlamaV2(self.config)

        if self.cache_8bit:
            self.cache = ExLlamaV2Cache_8bit(self.base, lazy=self.cache_lazy)
        else:
            self.cache = ExLlamaV2Cache(self.base, lazy=self.cache_lazy)

        if self.cache_lazy:
            self.base.load_autosplit(self.cache)
        else:
            self.base.load(gpu_split=self.gpu_split)

        self.tokenizer = ExLlamaV2Tokenizer(self.config)
        self.generator = ExLlamaV2StreamingGenerator(self.base, self.cache, self.tokenizer)

    def unload(self):
        self.base = None
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
                "temperature": ("FLOAT", {"default": 1, "max": 2, "step": 0.01}),
                "temperature_last": ("BOOLEAN", {"default": True}),
                "min_p": ("FLOAT", {"default": 0.1, "max": 1, "step": 0.01}),
                "top_p": ("FLOAT", {"default": 1, "max": 1, "step": 0.01}),
                "typical_p": ("FLOAT", {"default": 1, "max": 1, "step": 0.01}),
                "top_k": ("INT", {"max": 200}),
                "rep_penalty": ("FLOAT", {"default": 1, "min": 1, "max": 2, "step": 0.01}),
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
        temperature_last,
        min_p,
        top_p,
        typical_p,
        top_k,
        rep_penalty,
        seed,
        text,
        info=None,
        id=None,
    ):
        if not text:
            return ("",)

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
        torch.manual_seed(seed)
        random.seed(seed)

        settings = ExLlamaV2Sampler.Settings()
        settings.temperature = temperature
        settings.temperature_last = temperature_last
        settings.min_p = min_p
        settings.top_p = top_p
        settings.typical = typical_p
        settings.top_k = top_k
        settings.token_repetition_penalty = rep_penalty

        model.generator.begin_stream(input, settings, token_healing=True)
        progress = ProgressBar(max_tokens)
        start = time()
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
