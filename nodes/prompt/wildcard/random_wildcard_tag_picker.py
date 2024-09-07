import random


class RandomWildcardTagPicker:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "wildcard": ("STRING", {"default": "elements", "multiline": False}),
                "tag_amount": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "display": "number"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("random_tags", "next_seed")

    FUNCTION = "choose_random_tags"

    CATEGORY = "GR85/Prompt/Wildcard"

    def choose_random_tags(self, seed, wildcard, tag_amount):
        try:
            with open(f"ComfyUI/custom_nodes/GR85/wildcards/{wildcard}.txt", "r") as file:
                elements = file.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"No file found for wildcard: {wildcard}")

        result = []
        for element in elements:
            parts = element.split(':')
            if len(parts) == 2: # Check if we have two parts
                amount_str, name = parts
                amount = int(amount_str)
                result.extend([name.strip()] * amount)
            else:
                result.append(element.strip())
        random.seed(seed)
        chosen_elements = random.sample(result, tag_amount)

        # Random number between 0 and 0xffffffffffffffff
        next_seed = random.randint(0, 0xffffffffffffffff)

        return ", ".join(chosen_elements), next_seed
