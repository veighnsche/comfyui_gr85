import yaml
import random


class RandomElements:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "elements_amount": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "display": "number"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("random_elements",)

    FUNCTION = "choose_random_elements"

    CATEGORY = "GR85/Prompt/Wildcard"

    def choose_random_elements(self, seed, elements_amount):
        with open("ComfyUI/custom_nodes/GR85/wildcards/elements.txt", "r") as file:
            elements = file.readlines()
        result = []
        for element in elements:
            parts = element.split(':')
            if len(parts) == 2:  # Check if we have two parts
                amount_str, name = parts
                amount = int(amount_str)
                result.extend([name.strip()] * amount)
            else:
                result.append(element.strip())  # Handle elements without ':'
        random.seed(seed)
        chosen_elements = random.sample(result, elements_amount)
        return (", ".join(chosen_elements),)
