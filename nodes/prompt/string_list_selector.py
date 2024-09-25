class StringListSelector:
    """
    Selects a sublist of strings from the input list, starting at 'from_index' and taking 'amount' elements.
    The output is always a list, even if amount is 0 or 1.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "strings": ("STRING", {"default": ""}),
                "from_index": ("INT", {"default": 0, "min": 0}),
                "amount": ("INT", {"default": 1, "min": 0}),
            }
        }

    RETURN_TYPES = ("LIST",)
    OUTPUT_IS_LIST = (True,)

    FUNCTION = "select_strings"
    CATEGORY = "GR85/Prompt"

    def select_strings(self, strings, from_index, amount):
        # Ensure from_index is within bounds
        from_index = max(0, from_index)
        from_index = min(from_index, len(strings))  # Prevent index out of range

        # Calculate to_index ensuring it doesn't exceed the list length
        to_index = min(from_index + amount, len(strings))

        # Slice the list
        selected_strings = strings[from_index:to_index]

        # Ensure the output is always a list
        return (selected_strings,)
