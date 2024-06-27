import re


class StrSafe:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "multiline": True,
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("safe_text",)
    FUNCTION = "safe"
    CATEGORY = "GR85/Utils"

    def safe(self, text):
        """
        Replace all the special characters with underscores, excluding slashes.
        Then replace all the double and triple underscores with a single underscore.
        Then limit the number of characters to filename.png limits, which is 250.
        Then return the safe text.
        """
        replace_chars = ' :;,-+?!=@#$%^&*()[]{<>\\|~`.'
        for char in replace_chars:
            text = text.replace(char, '_')
        text = re.sub('_+', '_', text)  # Replace multiple underscores with single
        text = text[:250]  # Limit the number of characters to 250
        return (text, )


