from .nodes import Generator, Loader

NODE_CLASS_MAPPINGS = {
    "ZuellniExLlamaGenerator": Generator,
    "ZuellniExLlamaLoader": Loader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZuellniExLlamaGenerator": "ExLlama Generator",
    "ZuellniExLlamaLoader": "ExLlama Loader",
}
