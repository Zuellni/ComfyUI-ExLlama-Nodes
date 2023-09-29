from .nodes import Generator, Loader, Previewer, Replacer

NODE_CLASS_MAPPINGS = {
    "ZuellniExLlamaLoader": Loader,
    "ZuellniExLlamaGenerator": Generator,
    "ZuellniTextPreviewer": Previewer,
    "ZuellniTextReplacer": Replacer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZuellniExLlamaLoader": "ExLlama Loader",
    "ZuellniExLlamaGenerator": "ExLlama Generator",
    "ZuellniTextPreviewer": "Preview Text",
    "ZuellniTextReplacer": "Replace Text",
}

WEB_DIRECTORY = "."
