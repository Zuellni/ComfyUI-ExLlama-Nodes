import gc
import random
from time import time

import torch
from comfy.model_management import soft_empty_cache
from comfy.utils import ProgressBar
from exllamav2 import ExLlamaV2, ExLlamaV2Cache_8bit, ExLlamaV2Config, ExLlamaV2Tokenizer
from exllamav2.generator import ExLlamaV2Sampler, ExLlamaV2StreamingGenerator


class Loader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_dir": ("STRING", {"default": ""}),
                "max_seq_len": ("INT", {"default": 2048, "max": 8192}),
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

    def process(self, model_dir, max_seq_len):
        self.unload()
        self.config = ExLlamaV2Config()
        self.config.model_dir = model_dir
        self.config.prepare()

        if max_seq_len:
            self.config.max_seq_len = max_seq_len

        self.tokenizer = ExLlamaV2Tokenizer(self.config)
        self.load()

        return (self,)

    def load(self):
        if not self.base:
            self.base = ExLlamaV2(self.config)
            self.base.load()
            self.cache = ExLlamaV2Cache_8bit(self.base)
            self.generator = ExLlamaV2StreamingGenerator(self.base, self.cache, self.tokenizer)

    def unload(self):
        self.base = None
        self.cache = None
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
                "stop_on_newline": ("BOOLEAN", {"default": False}),
                "max_new_tokens": ("INT", {"default": 128, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.7, "max": 2, "step": 0.01}),
                "top_k": ("INT", {"default": 20, "max": 200}),
                "top_p": ("FLOAT", {"default": 0.9, "max": 1, "step": 0.01}),
                "typical_p": ("FLOAT", {"default": 1, "max": 1, "step": 0.01}),
                "penalty": ("FLOAT", {"default": 1.15, "min": 1, "max": 2, "step": 0.01}),
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
        stop_on_newline,
        max_new_tokens,
        temperature,
        top_k,
        top_p,
        typical_p,
        penalty,
        seed,
        text,
        info=None,
        id=None,
    ):
        if not text:
            return ("",)

        model.load()
        input = model.tokenizer.encode(text)
        stop_conditions = [model.tokenizer.eos_token_id]

        if not max_new_tokens:
            max_new_tokens = model.config.max_seq_len - input.shape[-1]

        if stop_on_newline:
            stop_conditions.append(model.tokenizer.newline_token_id)

        model.generator.set_stop_conditions(stop_conditions)
        random.seed(seed)

        settings = ExLlamaV2Sampler.Settings()
        settings.temperature = temperature
        settings.top_k = top_k
        settings.top_p = top_p
        settings.typical = typical_p
        settings.token_repetition_penalty = penalty

        model.generator.begin_stream(input, settings, token_healing=True)
        progress = ProgressBar(max_new_tokens)
        start = time()
        eos = False
        output = ""
        tokens = 0

        while not eos and tokens < max_new_tokens:
            chunk, eos, _ = model.generator.stream()
            progress.update(1)
            output += chunk
            tokens += 1

        output = output.strip()
        total = round(time() - start, 2)
        speed = round(tokens / total, 2)
        print(f"Output generated in {total} seconds ({tokens} tokens, {speed} tokens/s)")

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
