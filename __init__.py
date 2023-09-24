from .nodes import Generator, Loader, Lora, Previewer

NODE_CLASS_MAPPINGS = {
    "ZuellniExLlamaLoader": Loader,
    "ZuellniExLlamaLora": Lora,
    "ZuellniExLlamaGenerator": Generator,
    "ZuellniExLlamaPreviewer": Previewer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZuellniExLlamaLoader": "ExLlama Loader",
    "ZuellniExLlamaLora": "ExLlama LoRA",
    "ZuellniExLlamaGenerator": "ExLlama Generator",
    "ZuellniExLlamaPreviewer": "ExLlama Previewer",
}

WEB_DIRECTORY = "."
