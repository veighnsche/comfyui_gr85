import random


class RandomRatio:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "first_width": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "first_height": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),

                "second_width": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "second_height": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")

    FUNCTION = "random_ratio"

    CATEGORY = "GR85/Resolution"

    def random_ratio(self, seed, first_width, first_height, second_width, second_height):
        """
        Calculates a random ratio between a min and max ratio.

        Args:
          seed: The random number seed.
          first_width: The minimum width for the ratio.
          first_height: The minimum height for the ratio.
          second_width: The maximum width for the ratio.
          second_height: The maximum height for the ratio.

        Returns:
          A tuple containing the random width and height of the ratio.
        """
        random.seed(seed)

        min_ratio = min(first_width / first_height, second_width / second_height)
        max_ratio = max(first_width / first_height, second_width / second_height)

        random_ratio = random.uniform(min_ratio, max_ratio)

        # Converting the ratio to natural numbers for width and height
        if random_ratio >= 1:
            width = int(round(random_ratio * 100))
            height = 100
        else:
            width = 100
            height = int(round(100 / random_ratio))

        return width, height
