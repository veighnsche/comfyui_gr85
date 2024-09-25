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
        Trim spaces at the beginning and end, convert to lowercase,
        replace multiple underscores with a single underscore,
        and limit the number of characters to 250.
        """
        import re
        # Trim spaces at the beginning and end
        text = text.strip()
        # Convert to lowercase
        text = text.lower()
        # Replace all special characters with underscores
        replace_chars = ' :;,-+?!=@#$%^&*()[]{<>\\|~`.'
        for char in replace_chars:
            text = text.replace(char, '_')
        # Replace multiple underscores with single underscore
        text = re.sub('_+', '_', text)
        # Limit the number of characters to 250
        text = text[:250]
        return (text,)
