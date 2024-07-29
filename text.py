import string

_CATEGORY = "Zuellni/Text"
_MAPPING = "ZuellniText"


class Convert:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "strip": (("punctuation", "whitespace", "both", "none"),),
                "case": (("lower", "upper", "capitalize", "title", "none"),),
            },
        }

    CATEGORY = _CATEGORY
    FUNCTION = "convert"
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def convert(self, text, strip, case):
        if strip == "both":
            text = text.strip(string.punctuation + string.whitespace)
            text = " ".join(text.split()).strip()
        elif strip != "none":
            text = text.strip(getattr(string, strip))

        if case == "title":
            text = string.capwords(text)
        elif case != "none":
            text = getattr(text, case)()

        return (text,)


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
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "output": ("STRING", {"multiline": True}),
            },
        }

    CATEGORY = _CATEGORY
    FUNCTION = "preview"
    OUTPUT_NODE = True
    RETURN_TYPES = ()

    def preview(self, text, output):
        return {"ui": {"text": [text]}}


class Replace:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "count": ("INT", {"default": 1, "min": 1, "max": 26}),
                "text": ("STRING", {"multiline": True}),
            },
        }

    CATEGORY = _CATEGORY
    FUNCTION = "replace"
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def replace(self, count, text="", **kwargs):
        for index in range(count):
            key = chr(index + 97)

            if key in kwargs and kwargs[key]:
                text = text.replace(f"{{{key}}}", kwargs[key])

        return (text,)


class String:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"text": ("STRING", {"multiline": True})}}

    CATEGORY = _CATEGORY
    FUNCTION = "get"
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def get(self, text):
        return (text,)


NODE_CLASS_MAPPINGS = {
    f"{_MAPPING}Convert": Convert,
    f"{_MAPPING}Message": Message,
    f"{_MAPPING}Preview": Preview,
    f"{_MAPPING}Replace": Replace,
    f"{_MAPPING}String": String,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    f"{_MAPPING}Convert": "Convert",
    f"{_MAPPING}Message": "Message",
    f"{_MAPPING}Preview": "Preview",
    f"{_MAPPING}Replace": "Replace",
    f"{_MAPPING}String": "String",
}

WEB_DIRECTORY = "."
