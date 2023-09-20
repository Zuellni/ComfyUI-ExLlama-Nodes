from pathlib import Path

import torch
from comfy.utils import ProgressBar
from comfy.model_management import soft_empty_cache
from exllama.alt_generator import ExLlamaAltGenerator
from exllama.lora import ExLlamaLora
from exllama.model import ExLlama, ExLlamaCache, ExLlamaConfig
from exllama.tokenizer import ExLlamaTokenizer


class Generator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("GPTQ",),
                "stop_on_newline": ([False, True], {"default": False}),
                "max_tokens": ("INT", {"default": 128, "min": 1, "max": 8192}),
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
        typical_p,
        penalty,
        seed,
        prompt,
    ):
        progress = ProgressBar(max_tokens)
        prompt = prompt.strip()
        torch.manual_seed(seed)

        if not prompt:
            return ("",)

        model["settings"].temperature = temperature
        model["settings"].top_k = top_k
        model["settings"].top_p = top_p
        model["settings"].typical = typical_p
        model["settings"].token_repetition_penalty_max = penalty
        stop_conditions = [model["generator"].tokenizer.eos_token_id]

        if stop_on_newline:
            stop_conditions.append(model["generator"].tokenizer.newline_token_id)

        model["generator"].begin_stream(
            prompt=prompt,
            stop_conditions=stop_conditions,
            max_new_tokens=max_tokens,
            gen_settings=model["settings"],
        )

        eos = False
        text = ""

        while not eos:
            chunk, eos = model["generator"].stream()
            progress.update(1)
            text += chunk

        progress.update_absolute(max_tokens)
        text = text.strip()
        print(text)
        return (text,)


class Loader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_dir": ("STRING", {"default": ""}),
                "lora_dir": ("STRING", {"default": ""}),
                "max_seq_len": ("INT", {"default": 2048, "min": 1, "max": 8192}),
            },
        }

    CATEGORY = "Zuellni/ExLlama"
    FUNCTION = "load"
    RETURN_NAMES = ("MODEL",)
    RETURN_TYPES = ("GPTQ",)

    def load(self, model_dir, lora_dir, max_seq_len):
        soft_empty_cache()

        model_dir = Path(model_dir).expanduser()
        config = ExLlamaConfig(model_dir / "config.json")
        config.model_path = model_dir.glob("*.safetensors")
        config.max_seq_len = max_seq_len

        model = ExLlama(config)
        cache = ExLlamaCache(model)
        tokenizer = ExLlamaTokenizer(str(model_dir / "tokenizer.model"))
        generator = ExLlamaAltGenerator(model, tokenizer, cache)
        settings = ExLlamaAltGenerator.Settings()

        if lora_dir:
            lora_dir = Path(lora_dir).expanduser()
            lora_config = str(lora_dir / "adapter_config.json")
            lora_model = str(lora_dir / "adapter_model.bin")
            lora = ExLlamaLora(model, lora_config, lora_model)
            settings.lora = lora

        return ({"generator": generator, "settings": settings},)


class Previewer:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"text": ("STRING", {"forceInput": True})}}

    CATEGORY = "Zuellni/ExLlama"
    FUNCTION = "preview"
    OUTPUT_NODE = True
    RETURN_TYPES = ()

    def preview(self, text):
        return {"ui": {"text": [text]}}
