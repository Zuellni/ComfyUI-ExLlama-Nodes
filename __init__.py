from .nodes import Generator, Loader, Previewer

NODE_CLASS_MAPPINGS = {
    "ZuellniExLlamaLoader": Loader,
    "ZuellniExLlamaGenerator": Generator,
    "ZuellniExLlamaPreviewer": Previewer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZuellniExLlamaLoader": "ExLlama Loader",
    "ZuellniExLlamaGenerator": "ExLlama Generator",
    "ZuellniExLlamaPreviewer": "ExLlama Previewer",
}

WEB_DIRECTORY = "."
