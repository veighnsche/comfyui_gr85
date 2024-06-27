import re


class TagInjector:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "template": ("STRING", {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_name": ('STRING', {"default": "elements"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("tagged_text", "placeholders")
    FUNCTION = "inject_tag"
    CATEGORY = "GR85/Prompt"

    def inject_tag(self, template, tag_name, tag):
        data = {tag_name: tag}
        placeholders = re.findall(r'__(.*?)__', template)
        data_with_defaults = {key: data.get(key, f"__{key}__") for key in placeholders}
        # use regular string replace instead of format
        for key, value in data_with_defaults.items():
            template = template.replace(f"__{key}__", value)
        return template, placeholders
