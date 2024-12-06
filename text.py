import string

_CATEGORY = "zuellni/text"
_MAPPING = "ZuellniText"


class Clean:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "", "forceInput": True}),
                "strip": (
                    ("both", "punctuation", "whitespace", "none"),
                    {"default": "both"},
                ),
                "case": (
                    ("lower", "upper", "capitalize", "title", "none"),
                    {"default": "lower"},
                ),
                "fix": ("BOOLEAN", {"default": True}),
            }
        }

    CATEGORY = _CATEGORY
    FUNCTION = "clean"
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def clean(self, text, strip, case, fix):
        if strip == "both":
            text = text.strip(string.punctuation + string.whitespace)
        elif strip != "none":
            text = text.strip(getattr(string, strip))

        if case == "title":
            text = string.capwords(text)
        elif case != "none":
            text = getattr(text, case)()

        if fix:
            text = "\n".join([t for t in text.splitlines() if t])
            text = " ".join(text.split())

        return (text,)


class Message:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "role": (("system", "user", "assistant"), {"default": "system"}),
                "content": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {"messages": ("EXL_MESSAGES",)},
        }

    CATEGORY = _CATEGORY
    FUNCTION = "add"
    RETURN_NAMES = ("MESSAGES",)
    RETURN_TYPES = ("EXL_MESSAGES",)

    def add(self, role, content, messages=[]):
        return (messages + [{"role": role, "content": content}],)


class Preview:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "", "forceInput": True}),
                "print_to_console": ("BOOLEAN", {"default": False}),
                "output": ("STRING", {"default": "", "multiline": True}),
            }
        }

    CATEGORY = _CATEGORY
    FUNCTION = "preview"
    OUTPUT_NODE = True
    RETURN_TYPES = ()

    def preview(self, text, print_to_console, output):
        print_to_console and print(text)
        return {"ui": {"text": [text]}}


class Replace:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "count": ("INT", {"default": 1, "min": 1, "max": 26}),
                "text": ("STRING", {"default": "", "multiline": True}),
            }
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
        return {"required": {"text": ("STRING", {"default": "", "multiline": True})}}

    CATEGORY = _CATEGORY
    FUNCTION = "get"
    RETURN_NAMES = ("TEXT",)
    RETURN_TYPES = ("STRING",)

    def get(self, text):
        return (text,)


NODE_CLASS_MAPPINGS = {
    f"{_MAPPING}Clean": Clean,
    f"{_MAPPING}Message": Message,
    f"{_MAPPING}Preview": Preview,
    f"{_MAPPING}Replace": Replace,
    f"{_MAPPING}String": String,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    f"{_MAPPING}Clean": "Clean",
    f"{_MAPPING}Message": "Message",
    f"{_MAPPING}Preview": "Preview",
    f"{_MAPPING}Replace": "Replace",
    f"{_MAPPING}String": "String",
}

WEB_DIRECTORY = "."
