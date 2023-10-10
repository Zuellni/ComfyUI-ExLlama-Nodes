from comfy.model_management import InterruptProcessingException


class Condition:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("STRING", {"forceInput": True}),
                "condition": (["==", "!=", ">", ">=", "<", "<=", "in", "sw", "ew"],),
                "b": ("STRING", {"default": ""}),
            },
            "optional": {
                "text": ("STRING", {"forceInput": True, "multiline": True}),
            },
        }

    CATEGORY = "Zuellni/Text"
    FUNCTION = "condition"
    OUTPUT_Node = True
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def condition(self, a, condition, b, text=None):
        try:
            a = float(a)
            b = float(b)
        except:
            pass

        conditions = {
            "==": lambda: a == b,
            "!=": lambda: a != b,
            ">": lambda: a > b,
            ">=": lambda: a >= b,
            "<": lambda: a < b,
            "<=": lambda: a <= b,
            "in": lambda: str(a) in str(b),
            "sw": lambda: str(a).startswith(str(b)),
            "ew": lambda: str(a).endswith(str(b)),
        }

        if not conditions[condition]():
            raise InterruptProcessingException()

        return (text,)


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
    "ZuellniTextCondition": Condition,
    "ZuellniTextFormat": Format,
    "ZuellniTextPreview": Preview,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZuellniTextCondition": "Condition",
    "ZuellniTextFormat": "Format",
    "ZuellniTextPreview": "Preview",
}

WEB_DIRECTORY = "."
