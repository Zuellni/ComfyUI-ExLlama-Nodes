from gc import collect
from time import time

import torch
from comfy.model_management import soft_empty_cache
from comfy.utils import ProgressBar
from exllamav2 import ExLlamaV2, ExLlamaV2Cache, ExLlamaV2Config, ExLlamaV2Tokenizer
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
    FUNCTION = "load"
    RETURN_NAMES = ("MODEL",)
    RETURN_TYPES = ("EXL_MODEL",)

    def load(self, model_dir, max_seq_len):
        collect()
        soft_empty_cache()

        config = ExLlamaV2Config()
        config.model_dir = model_dir
        config.prepare()

        if max_seq_len:
            config.max_seq_len = max_seq_len

        model = ExLlamaV2(config)
        model.load()

        cache = ExLlamaV2Cache(model)
        tokenizer = ExLlamaV2Tokenizer(config)
        generator = ExLlamaV2StreamingGenerator(model, cache, tokenizer)

        return ((tokenizer, generator),)


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
                "stop_on_newline": ("BOOLEAN", {"default": False}),
                "allowed_strings": ("STRING", {"default": ""}),
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
        max_new_tokens,
        temperature,
        top_k,
        top_p,
        typical_p,
        penalty,
        seed,
        stop_on_newline,
        allowed_strings,
        text,
        info=None,
        id=None,
    ):
        text = text.strip()

        if not text:
            return ("",)

        tokenizer, generator = model
        text = tokenizer.encode(text)
        stop_conditions = [tokenizer.eos_token_id]

        if not max_new_tokens:
            max_new_tokens = tokenizer.config.max_seq_len - text.shape[-1]

        if stop_on_newline:
            stop_conditions.append(tokenizer.newline_token_id)

        settings = ExLlamaV2Sampler.Settings()
        settings.temperature = temperature
        settings.top_k = top_k
        settings.top_p = top_p
        settings.typical = typical_p
        settings.token_repetition_penalty = penalty

        if allowed_strings:
            strings = []

            for string in allowed_strings.split(","):
                string = string.strip()

                if "-" in string:
                    start, end = string.split("-")

                    if start.isdigit() and end.isdigit():
                        start, end = int(start), int(end)

                        if start <= end:
                            strings.extend(map(str, range(start, end + 1)))
                        else:
                            strings.extend(map(str, range(start, end - 1, -1)))
                    elif len(start) == 1 and len(end) == 1:
                        start, end = ord(start), ord(end)

                        if start <= end:
                            strings.extend(map(chr, range(start, end + 1)))
                        else:
                            strings.extend(map(chr, range(start, end + -1, -1)))
                    else:
                        strings.append(string)
                else:
                    strings.append(string)

            allowed_strings = strings
            allowed_tokens = tokenizer.encode(allowed_strings)
            max_new_tokens = allowed_tokens.shape[-1]

            vocab_size = tokenizer.config.vocab_size
            padding = vocab_size + (-vocab_size % 32)

            settings.token_bias = torch.full((padding,), float("-inf"))
            settings.token_bias[allowed_tokens] = 0

        torch.manual_seed(seed)
        generator.set_stop_conditions(stop_conditions)
        generator.begin_stream(text, settings)
        progress = ProgressBar(max_new_tokens)
        start = time()
        eos = False
        output = ""
        tokens = 0

        while not eos and tokens < max_new_tokens:
            chunk, eos, _ = generator.stream()

            if allowed_strings:
                c = (output + chunk).strip()

                if not any(c in s for s in allowed_strings):
                    break

            progress.update(1)
            output += chunk
            tokens += 1

        output = output.strip()
        total = round(time() - start, 2)
        speed = round(tokens / total, 2)
        print(f"Output generated in {total} seconds ({tokens} tokens, {speed} tokens/s)")

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
