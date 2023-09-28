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
    RETURN_TYPES = ("EXLLAMA_MODEL",)

    def load(self, model_dir, max_seq_len):
        config = ExLlamaV2Config()
        config.model_dir = model_dir
        config.prepare()
        config.max_seq_len = max_seq_len

        model = ExLlamaV2(config)
        model.load()

        tokenizer = ExLlamaV2Tokenizer(config)
        cache = ExLlamaV2Cache(model)
        generator = ExLlamaV2StreamingGenerator(model, cache, tokenizer)

        return (generator,)


class Generator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("EXLLAMA_MODEL",),
                "stop_on_newline": ([False, True], {"default": False}),
                "max_tokens": ("INT", {"default": 128, "min": 1, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.01}),
                "top_k": ("INT", {"default": 20, "min": 0, "max": 200}),
                "top_p": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 1.0, "step": 0.01}),
                "typical": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
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
        typical,
        penalty,
        seed,
        prompt,
    ):
        torch.manual_seed(seed)
        progress = ProgressBar(max_tokens)
        prompt = model.tokenizer.encode(prompt)
        stop_conditions = [model.tokenizer.eos_token_id]

        if stop_on_newline:
            stop_conditions += [model.tokenizer.newline_token_id]

        settings = ExLlamaV2Sampler.Settings()
        settings.temperature = temperature
        settings.top_k = top_k
        settings.top_p = top_p
        settings.typical = typical
        settings.token_repetition_penalty = penalty

        model.set_stop_conditions(stop_conditions)
        model.begin_stream(prompt, settings)
        eos = False
        tokens = 0
        text = ""

        while not eos and tokens < max_tokens:
            chunk, eos, _ = model.stream()
            progress.update(1)
            text += chunk
            tokens += 1

        return (text.strip(),)


class Previewer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "info": "EXTRA_PNGINFO",
                "id": "UNIQUE_ID",
            },
        }

    CATEGORY = "Zuellni/ExLlama"
    FUNCTION = "preview"
    OUTPUT_NODE = True
    RETURN_TYPES = ()

    def preview(self, text, info=None, id=None):
        if id and info and "workflow" in info:
            workflow = info["workflow"]
            node = next((n for n in workflow["nodes"] if str(n["id"]) == id), None)

            if node:
                node["widgets_values"] = [text]

        return {"ui": {"text": [text]}}
