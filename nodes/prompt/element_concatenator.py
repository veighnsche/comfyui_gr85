class ElementConcatenator:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "title_character_elements": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "multiline": True
                }),
                "random_elements": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "multiline": True
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("concatenated_elements",)

    FUNCTION = "concatenate_elements"

    CATEGORY = "GR85/Prompt"

    def concatenate_elements(self, title_character_elements, random_elements):
        return (f"{title_character_elements}, {random_elements}",)
