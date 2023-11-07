class Preview:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            }
        }

    CATEGORY = "Zuellni/Text"
    FUNCTION = "preview"
    OUTPUT_NODE = True
    RETURN_TYPES = ()

    def preview(self, text):
        return {"ui": {"text": [text]}}


class Replace:
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

    def replace(self, text, **inputs):
        for key, value in inputs.items():
            if value:
                text = text.replace(f"[{key}]", value)

        return (text,)


NODE_CLASS_MAPPINGS = {
    "ZuellniTextPreview": Preview,
    "ZuellniTextReplace": Replace,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZuellniTextPreview": "Preview",
    "ZuellniTextReplace": "Replace",
}

WEB_DIRECTORY = "."
