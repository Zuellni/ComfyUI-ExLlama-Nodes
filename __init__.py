from .nodes import Formatter, Generator, Loader, Previewer

NODE_CLASS_MAPPINGS = {
    "ZuellniExLlamaLoader": Loader,
    "ZuellniExLlamaGenerator": Generator,
    "ZuellniTextFormatter": Formatter,
    "ZuellniTextPreviewer": Previewer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZuellniExLlamaLoader": "ExLlama Loader",
    "ZuellniExLlamaGenerator": "ExLlama Generator",
    "ZuellniTextFormatter": "Format Text",
    "ZuellniTextPreviewer": "Preview Text",
}

WEB_DIRECTORY = "."
