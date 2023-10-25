import gc
import random
from time import time

import torch
from comfy.model_management import soft_empty_cache
from comfy.utils import ProgressBar
from exllamav2 import (
    ExLlamaV2,
    ExLlamaV2Cache_8bit,
    ExLlamaV2Config,
    ExLlamaV2Lora,
    ExLlamaV2Tokenizer,
)
from exllamav2.generator import ExLlamaV2Sampler, ExLlamaV2StreamingGenerator


class Model:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_dir": ("STRING", {"default": ""}),
                "max_seq_len": ("INT", {"default": 2048, "max": 8192}),
            },
        }

    CATEGORY = "Zuellni/ExLlama"
    FUNCTION = "prepare"
    RETURN_NAMES = ("MODEL",)
    RETURN_TYPES = ("EXL_MODEL",)

    def __init__(self):
        self.config = None
        self.base = None
        self.cache = None
        self.tokenizer = None
        self.generator = None

    def prepare(self, model_dir, max_seq_len):
        self.unload()

        self.config = ExLlamaV2Config()
        self.config.model_dir = model_dir
        self.config.prepare()

        if max_seq_len:
            self.config.max_seq_len = max_seq_len

        self.load()

        return ((self, []),)

    def load(self):
        if not self.base:
            self.base = ExLlamaV2(self.config)
            self.base.load()

            self.cache = ExLlamaV2Cache_8bit(self.base)
            self.tokenizer = ExLlamaV2Tokenizer(self.config)

            self.generator = ExLlamaV2StreamingGenerator(
                self.base,
                self.cache,
                self.tokenizer,
            )

        return self.base

    def unload(self):
        if self.base:
            self.base.unload()

        del self.base, self.cache, self.tokenizer, self.generator
        gc.collect()
        soft_empty_cache()

        self.base = None
        self.cache = None
        self.tokenizer = None
        self.generator = None


class Lora:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("EXL_MODEL",),
                "lora_dir": ("STRING", {"default": ""}),
            },
        }

    CATEGORY = "Zuellni/ExLlama"
    FUNCTION = "load"
    RETURN_NAMES = ("MODEL",)
    RETURN_TYPES = ("EXL_MODEL",)

    def load(self, model, lora_dir):
        model, loras = model

        lora = ExLlamaV2Lora.from_directory(model.load(), lora_dir)
        loras = loras.copy()
        loras.append(lora)

        return ((model, loras),)


class Generator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("EXL_MODEL",),
                "max_new_tokens": ("INT", {"default": 128, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.7, "max": 2, "step": 0.01}),
                "top_k": ("INT", {"default": 20, "max": 200}),
                "top_p": ("FLOAT", {"default": 0.9, "max": 1, "step": 0.01}),
                "typical_p": ("FLOAT", {"default": 1, "max": 1, "step": 0.01}),
                "penalty": ("FLOAT", {"default": 1.15, "min": 1, "max": 2, "step": 0.01}),
                "seed": ("INT", {"max": 2**64 - 1}),
                "unload": ("BOOLEAN", {"default": False}),
                "stop_on_newline": ("BOOLEAN", {"default": False}),
                "allow_strings": ("BOOLEAN", {"default": False}),
                "strings": ("STRING", {"default": ""}),
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

    def format(self, strings):
        list = []

        for string in strings.split(","):
            if "-" in string:
                start, end = string.split("-")

                if start.isdigit() and end.isdigit():
                    start, end = int(start), int(end)

                    if start <= end:
                        list.extend(map(str, range(start, end + 1)))
                    else:
                        list.extend(map(str, range(start, end - 1, -1)))
                elif len(start) == 1 and len(end) == 1:
                    start, end = ord(start), ord(end)

                    if start <= end:
                        list.extend(map(chr, range(start, end + 1)))
                    else:
                        list.extend(map(chr, range(start, end + -1, -1)))
                else:
                    list.append(string)
            else:
                list.append(string)

        return list

    def generate(
        self,
        model,
        max_new_tokens,
        temperature,
        top_k,
        top_p,
        typical_p,
        penalty,
        seed,
        unload,
        stop_on_newline,
        allow_strings,
        strings,
        text,
        info=None,
        id=None,
    ):
        if not text:
            return ("",)

        model, loras = model

        model.load()
        text = model.tokenizer.encode(text)
        stop_conditions = [model.tokenizer.eos_token_id]

        if not max_new_tokens:
            max_new_tokens = model.config.max_seq_len - text.shape[-1]

        if stop_on_newline:
            stop_conditions.append(model.tokenizer.newline_token_id)

        settings = ExLlamaV2Sampler.Settings()
        settings.temperature = temperature
        settings.top_k = top_k
        settings.top_p = top_p
        settings.typical = typical_p
        settings.token_repetition_penalty = penalty

        if strings:
            strings = self.format(strings)
            tokens = model.tokenizer.encode(strings)
            vocab_size = model.config.vocab_size
            padding = vocab_size + (-vocab_size % 32)

            if allow_strings:
                settings.token_bias = torch.full((padding,), float("-inf"))
                settings.token_bias[tokens] = 0
                max_new_tokens = tokens.shape[-1]
            else:
                settings.token_bias = torch.zeros((padding,))
                settings.token_bias[tokens] = float("-inf")

        random.seed(seed)
        model.generator.set_stop_conditions(stop_conditions)
        model.generator.begin_stream(text, settings, loras=loras)
        progress = ProgressBar(max_new_tokens)
        start = time()
        eos = False
        output = ""
        tokens = 0

        while not eos and tokens < max_new_tokens:
            chunk, eos, _ = model.generator.stream()

            if strings and allow_strings:
                c = (output + chunk).strip()

                if not any(c in s for s in strings):
                    break

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
    "ZuellniExLlamaModel": Model,
    "ZuellniExLlamaLora": Lora,
    "ZuellniExLlamaGenerator": Generator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZuellniExLlamaModel": "Model",
    "ZuellniExLlamaLora": "LoRA",
    "ZuellniExLlamaGenerator": "Generator",
}
