class GenerateDefaultCLIPValues:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {}  # No input needed for this node

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("default_clip_values_str",)

    FUNCTION = "generate_default_clip_values"

    CATEGORY = "GR85/Prompt"

    def generate_default_clip_values(self):
        # Generate a string with 24 default values, all set to 1.0
        default_clip_values_str = ",".join(["1.0"] * 24)
        return (default_clip_values_str,)
