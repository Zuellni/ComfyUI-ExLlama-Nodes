from .nodes import Generator, Loader, Lora, Previewer

NODE_CLASS_MAPPINGS = {
    "ZuellniExLlamaLoader": Loader,
    "ZuellniExLlamaLoraLoader": Lora,
    "ZuellniExLlamaGenerator": Generator,
    "ZuellniExLlamaPreviewer": Previewer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZuellniExLlamaLoader": "ExLlama Loader",
    "ZuellniExLlamaLoraLoader": "ExLlama LoRA Loader",
    "ZuellniExLlamaGenerator": "ExLlama Generator",
    "ZuellniExLlamaPreviewer": "ExLlama Previewer",
}

WEB_DIRECTORY = "."
