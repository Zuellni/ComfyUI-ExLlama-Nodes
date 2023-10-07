from time import time

import torch
from comfy.utils import ProgressBar
from exllamav2 import ExLlamaV2, ExLlamaV2Cache, ExLlamaV2Config, ExLlamaV2Tokenizer
from exllamav2.generator import ExLlamaV2Sampler, ExLlamaV2StreamingGenerator


class Loader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_dir": ("STRING", {"default": ""}),
                "max_seq_len": ("INT", {"default": 2048, "min": 1, "max": 8192}),
            },
        }

    CATEGORY = "Zuellni/ExLlama"
    FUNCTION = "load"
    RETURN_NAMES = ("MODEL",)
    RETURN_TYPES = ("EL_MODEL",)

    def load(self, model_dir, max_seq_len):
        config = ExLlamaV2Config()
        config.model_dir = model_dir
        config.prepare()
        config.max_seq_len = max_seq_len

        model = ExLlamaV2(config)
        model.load()

        cache = ExLlamaV2Cache(model)
        tokenizer = ExLlamaV2Tokenizer(config)
        generator = ExLlamaV2StreamingGenerator(model, cache, tokenizer)
        settings = ExLlamaV2Sampler.Settings()

        return ((tokenizer, generator, settings),)


class Generator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("EL_MODEL",),
                "stop_on_newline": ((False, True),),
                "max_tokens": ("INT", {"default": 128, "min": 1, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.7, "max": 2, "step": 0.01}),
                "top_k": ("INT", {"default": 20, "max": 200}),
                "top_p": ("FLOAT", {"default": 0.9, "max": 1, "step": 0.01}),
                "typical": ("FLOAT", {"default": 1, "max": 1, "step": 0.01}),
                "penalty": ("FLOAT", {"default": 1.15, "min": 1, "max": 2, "step": 0.01}),
                "seed": ("INT", {"max": 2**64 - 1}),
                "text": ("STRING", {"multiline": True}),
            },
        }

    CATEGORY = "Zuellni/ExLlama"
    FUNCTION = "generate"
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def generate(
        self,
        model,
        stop_on_newline,
        max_tokens,
        temperature,
        top_k,
        top_p,
        typical,
        penalty,
        seed,
        text,
    ):
        tokenizer, generator, settings = model
        progress = ProgressBar(max_tokens)

        if not text:
            return ("",)

        prompt = tokenizer.encode(text)
        stop_conditions = [tokenizer.eos_token_id]
        stop_on_newline and stop_conditions.append(tokenizer.newline_token_id)
        generator.set_stop_conditions(stop_conditions)

        settings.temperature = temperature
        settings.top_k = top_k
        settings.top_p = top_p
        settings.typical = typical
        settings.token_repetition_penalty = penalty

        torch.manual_seed(seed)
        generator.begin_stream(prompt, settings)
        start = time()
        eos = False
        output = ""
        tokens = 0

        while not eos and tokens < max_tokens:
            chunk, eos, _ = generator.stream()
            progress.update(1)
            output += chunk
            tokens += 1

        total = round(time() - start, 2)
        speed = round(tokens / total, 2)

        print(f"Output generated in {total} seconds ({tokens} tokens, {speed} tokens/s)")
        return (output.strip(),)


NODE_CLASS_MAPPINGS = {
    "ZuellniExLlamaLoader": Loader,
    "ZuellniExLlamaGenerator": Generator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZuellniExLlamaLoader": "Loader",
    "ZuellniExLlamaGenerator": "Generator",
}
