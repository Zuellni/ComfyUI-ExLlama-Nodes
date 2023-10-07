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

    CATEGORY = "Zuellni/Text"
    FUNCTION = "preview"
    OUTPUT_NODE = True
    RETURN_TYPES = ()

    def preview(self, text, info=None, id=None):
        if id and info and "workflow" in info:
            nodes = info["workflow"]["nodes"]
            node = next((n for n in nodes if str(n["id"]) == id), None)

            if node:
                node["widgets_values"] = [text]

        return {"ui": {"text": [text]}}


class Replacer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            },
            "optional": {
                "a": ("STRING", {"forceInput": True, "multiline": True}),
                "b": ("STRING", {"forceInput": True, "multiline": True}),
                "c": ("STRING", {"forceInput": True, "multiline": True}),
                "d": ("STRING", {"forceInput": True, "multiline": True}),
            },
        }

    CATEGORY = "Zuellni/Text"
    FUNCTION = "replace"
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def replace(self, text, **vars):
        for key, value in vars.items():
            text = text.replace(f"[{key}]", value)

        return (text,)


NODE_CLASS_MAPPINGS = {
    "ZuellniTextPreviewer": Previewer,
    "ZuellniTextReplacer": Replacer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZuellniTextPreviewer": "Preview Text",
    "ZuellniTextReplacer": "Replace Text",
}

WEB_DIRECTORY = "."
