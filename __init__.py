from . import exllama, text

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
WEB_DIRECTORY = "."

for module in (exllama, text):
    NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
