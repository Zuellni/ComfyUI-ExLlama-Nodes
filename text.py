_CATEGORY = "Zuellni/Text"
_MAPPING = "ZuellniText"


class Message:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "role": (("system", "user", "assistant"),),
                "content": ("STRING", {"multiline": True}),
            },
            "optional": {"messages": ("EXL_MESSAGES",)},
        }

    CATEGORY = _CATEGORY
    FUNCTION = "append"
    RETURN_NAMES = ("MESSAGES",)
    RETURN_TYPES = ("EXL_MESSAGES",)

    def append(self, role, content, messages=[]):
        return (messages + [{"role": role, "content": content}],)


class Preview:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"text": ("STRING", {"forceInput": True})}}

    CATEGORY = _CATEGORY
    FUNCTION = "preview"
    OUTPUT_NODE = True
    RETURN_TYPES = ()

    def preview(self, text):
        return {"ui": {"text": [text]}}


class Replace:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"text": ("STRING", {"multiline": True})},
            "optional": {
                "a": ("STRING", {"forceInput": True, "multiline": True}),
                "b": ("STRING", {"forceInput": True, "multiline": True}),
                "c": ("STRING", {"forceInput": True, "multiline": True}),
                "d": ("STRING", {"forceInput": True, "multiline": True}),
            },
        }

    CATEGORY = _CATEGORY
    FUNCTION = "replace"
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def replace(self, text, **inputs):
        for key, value in inputs.items():
            if value:
                text = text.replace(f"[{key}]", value)

        return (text,)


NODE_CLASS_MAPPINGS = {
    f"{_MAPPING}Message": Message,
    f"{_MAPPING}Preview": Preview,
    f"{_MAPPING}Replace": Replace,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    f"{_MAPPING}Message": "Message",
    f"{_MAPPING}Preview": "Preview",
    f"{_MAPPING}Replace": "Replace",
}

WEB_DIRECTORY = "."
