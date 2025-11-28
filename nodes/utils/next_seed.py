import random


class NextSeed:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("next_seed",)
    FUNCTION = "next_seed"
    CATEGORY = "GR85/Random/Seed"

    def next_seed(self, seed):
        random.seed(seed)
        return (random.randint(0, 0xffffffffffffffff),)


