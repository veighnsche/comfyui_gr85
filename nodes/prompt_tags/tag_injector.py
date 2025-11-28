import re


class TagInjectorSingle:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template": ("STRING", {"multiline": True, "dynamicPrompts": True,
                                        "default": "__elements__"}),
            },
            "optional": {
                "tag_1": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_name_1": ('STRING', {"default": "elements"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("tagged_text", "placeholders")
    FUNCTION = "inject_tag"
    CATEGORY = "GR85/Prompt/Tags"

    def inject_tag(self, template, tag_1=None, tag_name_1="elements"):
        """
        Inject a single tag into the template based on the given tag name and value.
        """
        # Create a dictionary to hold the tag value for the tag name
        data = {tag_name_1: tag_1}

        # Find placeholders in the template (e.g., __location__)
        placeholders = re.findall(r'__(.*?)__', template)

        # Fill placeholders with the corresponding tag value or default to the placeholder itself
        data_with_defaults = {key: data.get(key, f"__{key}__") for key in placeholders}

        # Replace each placeholder in the template with the corresponding tag value
        for key, value in data_with_defaults.items():
            template = template.replace(f"__{key}__", value)

        # Return the modified template and the list of placeholders used
        return template, placeholders


class TagInjectorDuo:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template": ("STRING", {"multiline": True, "dynamicPrompts": True,
                                        "default": "__elements__"}),
            },
            "optional": {
                "tag_1": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_2": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_name_1": ('STRING', {"default": "elements"}),
                "tag_name_2": ('STRING', {"default": "stuff"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("tagged_text", "placeholders")
    FUNCTION = "inject_tag"
    CATEGORY = "GR85/Prompt"

    def inject_tag(self, template, tag_1=None, tag_2=None,
                   tag_name_1="elements", tag_name_2="stuff"):
        """
        Inject two tags into the template based on the given tag names and values.
        """
        # Create a dictionary to hold tag values for each tag name
        data = {tag_name_1: tag_1, tag_name_2: tag_2}

        # Find placeholders in the template (e.g., __location__, __weather__, etc.)
        placeholders = re.findall(r'__(.*?)__', template)

        # Fill placeholders with the corresponding tag value or default to the placeholder itself
        data_with_defaults = {key: data.get(key, f"__{key}__") for key in placeholders}

        # Replace each placeholder in the template with the corresponding tag value
        for key, value in data_with_defaults.items():
            template = template.replace(f"__{key}__", value)

        # Return the modified template and the list of placeholders used
        return template, placeholders


class TagInjector:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template": ("STRING", {"multiline": True, "dynamicPrompts": True,
                                        "default": "__elements__"}),
            },
            "optional": {
                "tag_1": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_2": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_3": ('STRING', {"forceInput": True, "multiline": True, "dynamicPrompts": True}),
                "tag_name_1": ('STRING', {"default": "elements"}),
                "tag_name_2": ('STRING', {"default": "stuff"}),
                "tag_name_3": ('STRING', {"default": "things"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("tagged_text", "placeholders")
    FUNCTION = "inject_tag"
    CATEGORY = "GR85/Prompt"

    def inject_tag(self, template, tag_1=None, tag_2=None, tag_3=None,
                   tag_name_1="elements", tag_name_2="stuff", tag_name_3="things"):
        """
        Inject tags into the template based on the given tag names and values.
        """

        # Create a dictionary to hold tag values for each tag name
        data = {
            tag_name_1: tag_1, tag_name_2: tag_2, tag_name_3: tag_3
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
