import random
from comfy_api.latest import io


class NextSeed(io.ComfyNode):
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

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="GR85_NextSeed",
            display_name="Next Seed",
            category="GR85/Random/Seed",
            inputs=[
                io.Int.Input(
                    "seed",
                    default=0,
                    min=0,
                    max=0xFFFFFFFFFFFFFFFF,
                ),
            ],
            outputs=[
                io.Int.Output(),
            ],
        )

    @classmethod
    def execute(
        cls,
        seed: int,
    ) -> io.NodeOutput:
        instance = cls()
        (value,) = instance.next_seed(seed=seed)
        return io.NodeOutput(value)

    def next_seed(self, seed):
        random.seed(seed)
        return (random.randint(0, 0xffffffffffffffff),)


