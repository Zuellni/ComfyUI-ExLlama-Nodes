import json
from pathlib import Path

import torch
from comfy.model_management import throw_exception_if_processing_interrupted
from comfy.utils import ProgressBar
from exllama.alt_generator import ExLlamaAltGenerator
from exllama.model import ExLlama, ExLlamaCache, ExLlamaConfig
from exllama.tokenizer import ExLlamaTokenizer


class Generator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("GPTQ",),
                "tokens": ("INT", {"default": 128, "min": 1, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.01}),
                "top_k": ("INT", {"default": 20, "min": 0, "max": 200}),
                "top_p": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 1.0, "step": 0.01}),
                "typical_p": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "penalty": ("FLOAT", {"default": 1.15, "min": 1.0, "max": 2.0, "step": 0.01}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**64 - 1}),
                "prompt": ("STRING", {"default": "", "multiline": True}),
            },
        }

    CATEGORY = "Zuellni/ExLlama"
    FUNCTION = "generate"
    OUTPUT_NODE = True
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def generate(self, model, tokens, temperature, top_k, top_p, typical_p, penalty, seed, prompt):
        progress = ProgressBar(tokens)

        def update(value):
            throw_exception_if_processing_interrupted()
            progress.update(value)

        settings = ExLlamaAltGenerator.Settings()
        settings.temperature = temperature
        settings.top_k = top_k
        settings.top_p = top_p
        settings.typical = typical_p
        settings.token_repetition_penalty_max = penalty

        torch.manual_seed(seed)
        stop_conditions = [model.tokenizer.eos_token_id, model.tokenizer.newline_token_id]
        model.begin_stream(prompt, stop_conditions, tokens, settings)

        eos = False
        output = ""

        while not eos:
            chunk, eos = model.stream()
            output += chunk
            progress.update(1)

        progress.update_absolute(tokens)
        output = output.strip()
        print(output)
        return (output,)


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
    RETURN_TYPES = ("GPTQ",)

    def load(self, model_dir, max_seq_len):
        model_dir = Path(model_dir).expanduser()

        config = ExLlamaConfig(model_dir / "config.json")
        config.model_path = model_dir.glob("*.safetensors")
        config.max_seq_len = max_seq_len

        model = ExLlama(config)
        cache = ExLlamaCache(model)

        # sentencepiece requires a string
        tokenizer = ExLlamaTokenizer(str(model_dir / "tokenizer.model"))
        generator = ExLlamaAltGenerator(model, tokenizer, cache)
        return (generator,)
