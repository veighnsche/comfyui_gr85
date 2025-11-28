import random
from comfy_api.latest import io

class RandomFloat(io.ComfyNode):
    """
    A ComfyUI node class that generates a random float based on given inputs.

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
                "min_value": ("FLOAT", {"default": 0.0, "min": -1e-10, "max": 1e10, "step": 0.0001, "display": "number"}),
                "max_value": ("FLOAT", {"default": 1.0, "min": -1e-10, "max": 1e10, "step": 0.0001, "display": "number"}),
                "decimal_places": ("INT", {"default": 10, "min": 0, "display": "number"}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("random_float",)

    FUNCTION = "generate_random_float"
    CATEGORY = "GR85/Random/Numbers"

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="GR85_RandomFloat",
            display_name="Random Float",
            category="GR85/Random/Numbers",
            inputs=[
                io.Int.Input(
                    "seed",
                    default=0,
                    min=0,
                ),
                io.Float.Input(
                    "min_value",
                    default=0.0,
                    min=-1e-10,
                    max=1e10,
                    step=0.0001,
                ),
                io.Float.Input(
                    "max_value",
                    default=1.0,
                    min=-1e-10,
                    max=1e10,
                    step=0.0001,
                ),
                io.Int.Input(
                    "decimal_places",
                    default=10,
                    min=0,
                ),
            ],
            outputs=[
                io.Float.Output(),
            ],
        )

    @classmethod
    def execute(
        cls,
        seed: int,
        min_value: float,
        max_value: float,
        decimal_places: int,
    ) -> io.NodeOutput:
        instance = cls()
        (value,) = instance.generate_random_float(
            seed=seed,
            min_value=min_value,
            max_value=max_value,
            decimal_places=decimal_places,
        )
        return io.NodeOutput(value)

    def generate_random_float(self, seed: int, min_value: float, max_value: float, decimal_places: int) -> tuple:
        """
        Generates a random float based on the given seed, min, max, and decimal places.

        Args:
            seed (int): The seed value for random number generation.
            min_value (float): The minimum value of the generated float.
            max_value (float): The maximum value of the generated float.
            decimal_places (int): The number of decimal places for the generated float.

        Returns:
            tuple: A tuple containing the generated random float.
        """
        random.seed(seed)
        random_float = round(random.uniform(min_value, max_value), decimal_places)
        return (random_float,)
