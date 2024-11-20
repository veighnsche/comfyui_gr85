from random import Random

class VerticalWildcardPicker:
    def __init__(self):
        pass

    """
    ComfyUI Custom Node
    Processes a vertical wildcard list using a seed for reproducibility.
    """

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Processed Prompt String",)
    OUTPUT_NODE = False
    FUNCTION = "process_vertical_wildcards"

    CATEGORY = "GR85/Prompt"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "wildcard_list": ('STRING', {'default': '', 'multiline': True, 'dynamicPrompts': False}),
                "seed": ('INT', {'default': 0, 'min': 0, 'max': 0xffffffffffffffff})
            }
        }

    @staticmethod
    def process_vertical_wildcards(wildcard_list, seed):
        """
        Processes each line in the vertical wildcard list directly, choosing options based on a seed.
        """
        rng = Random(seed)
        options = []

        # Read each line, parsing any counts and adding entries to the options list
        for line in wildcard_list.splitlines():
            line = line.strip()
            if ':' in line:
                count, element = line.split(':')
                options.extend([element] * int(count))  # Repeat the element as per the specified count
            else:
                options.append(line)  # Single occurrence for elements without count

        # Pick a random option from the list based on the seed
        if options:
            picked_option = options[rng.randint(0, len(options) - 1)]
        else:
            picked_option = ''  # Default to empty if no options

        return (picked_option,)
