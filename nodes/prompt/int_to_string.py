class IntToStringConverter:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "integer_value": ("INT", {"forceInput": True, "default": 0}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string_value",)

    FUNCTION = "convert"

    CATEGORY = "GR85/Prompt"

    def convert(self, integer_value):
        """
        Converts an integer to its string representation.
        """
        return (str(integer_value),)
