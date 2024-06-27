class ContainsWord:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "multiline": True,
                }),
                "words": ("STRING", {
                    "default": "",
                    "multiline": False
                }),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is_containing_the_word",)

    FUNCTION = "contains_word"

    CATEGORY = "GR85/Prompt"

    def contains_word(self, text, words):
        """
        Rules:
        - The word should be case-insensitive
        - Multiple words are separated by commas
        - The word should be surrounded by spaces or at the beginning or end of the text
        """
        split_words = words.split(",")
        for word in split_words:
            word = word.strip()
            # What is strip in python? answer:
            # https://www.w3schools.com/python/ref_string_strip.asp
            if word.lower() in text.lower():
                return True,
        return False,
