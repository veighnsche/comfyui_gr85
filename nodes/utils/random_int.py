import random

class RandomInt:
    """
    A ComfyUI node class that generates a random integer based on given inputs.

    Attributes:
        INPUT_TYPES (dict): Defines the required and optional input types for the node.
        RETURN_TYPES (tuple): Specifies the types of values returned by the node.
        RETURN_NAMES (tuple): Specifies the names of the returned values for better identification.
        FUNCTION (str): The function name used for processing parameters.
        CATEGORY (str): The category under which this node is classified.
    """

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "display": "number"}),
                "min_value": ("INT", {"default": 0, "min": -1e10, "max": 1e10, "display": "number"}),
                "max_value": ("INT", {"default": 100, "min": -1e10, "max": 1e10, "display": "number"}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("random_int",)

    FUNCTION = "generate_random_int"
    CATEGORY = "GR85/Utils"

    def generate_random_int(self, seed: int, min_value: int, max_value: int) -> tuple:
        """
        Generates a random integer based on the given seed, min, and max values.

        Args:
            seed (int): The seed value for random number generation.
            min_value (int): The minimum value of the generated integer.
            max_value (int): The maximum value of the generated integer.

        Returns:
            tuple: A tuple containing the generated random integer.
        """
        random.seed(seed)
        random_int = random.randint(min_value, max_value)
        return (random_int,)
