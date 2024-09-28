import re


class TagInjector:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"forceInput": True, "default": 0}),
                "template": ("STRING", {"multiline": True, "dynamicPrompts": True,
                                        "default": "In a __location__ under a __weather__ sky, a __personality__ person shows __emotion__ while wearing __style__. The __time__ is perfect for a __action__ amidst __mood__."}),
            },
            "optional": {
                "tag_1": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_2": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_3": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_4": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_5": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_6": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_7": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_8": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_9": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_10": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_name_1": ('STRING', {"default": "location"}),
                "tag_name_2": ('STRING', {"default": "color"}),
                "tag_name_3": ('STRING', {"default": "object"}),
                "tag_name_4": ('STRING', {"default": "emotion"}),
                "tag_name_5": ('STRING', {"default": "weather"}),
                "tag_name_6": ('STRING', {"default": "personality"}),
                "tag_name_7": ('STRING', {"default": "time"}),
                "tag_name_8": ('STRING', {"default": "action"}),
                "tag_name_9": ('STRING', {"default": "style"}),
                "tag_name_10": ('STRING', {"default": "mood"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("tagged_text", "placeholders")
    FUNCTION = "inject_tag"
    CATEGORY = "GR85/Prompt"

    def inject_tag(self, seed, template, tag_1=None, tag_2=None, tag_3=None, tag_4=None, tag_5=None,
                   tag_6=None, tag_7=None, tag_8=None, tag_9=None, tag_10=None,
                   tag_name_1="location", tag_name_2="color", tag_name_3="object", tag_name_4="emotion",
                   tag_name_5="weather", tag_name_6="personality", tag_name_7="time", tag_name_8="action",
                   tag_name_9="style", tag_name_10="mood"):
        """
        Inject tags into the template based on the given tag names and values.
        """

        # Create a dictionary to hold tag values for each tag name
        data = {
            tag_name_1: tag_1, tag_name_2: tag_2, tag_name_3: tag_3, tag_name_4: tag_4,
            tag_name_5: tag_5, tag_name_6: tag_6, tag_name_7: tag_7, tag_name_8: tag_8,
            tag_name_9: tag_9, tag_name_10: tag_10
        }

        # Find placeholders in the template (e.g., __location__, __weather__, etc.)
        placeholders = re.findall(r'__(.*?)__', template)

        # Fill placeholders with the corresponding tag value or default to the placeholder itself
        data_with_defaults = {key: data.get(key, f"__{key}__") for key in placeholders}

        # Replace each placeholder in the template with the corresponding tag value
        for key, value in data_with_defaults.items():
            template = template.replace(f"__{key}__", value)

        # Return the modified template and the list of placeholders used
        return template, placeholders
