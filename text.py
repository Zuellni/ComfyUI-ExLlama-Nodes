class Format:
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
    FUNCTION = "format"
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def format(self, text, **vars):
        for key, value in vars.items():
            if value:
                text = text.replace(f"[{key}]", value)

        return (text,)


class Preview:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"text": ("STRING", {"forceInput": True})}}

    CATEGORY = "Zuellni/Text"
    FUNCTION = "preview"
    OUTPUT_NODE = True
    RETURN_TYPES = ()

    def preview(self, text):
        return {"ui": {"text": [text]}}


NODE_CLASS_MAPPINGS = {
    "ZuellniTextFormat": Format,
    "ZuellniTextPreview": Preview,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZuellniTextFormat": "Format",
    "ZuellniTextPreview": "Preview",
}

WEB_DIRECTORY = "."
