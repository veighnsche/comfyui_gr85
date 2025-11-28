import math
from comfy_api.latest import io


class ImageDimensionResizer(io.ComfyNode):
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "original_width": ("INT", {
                    "forceInput": True,
                    "default": 512,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "original_height": ("INT", {
                    "forceInput": True,
                    "default": 512,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "target_dimensions": (["512x512", "512x768", "768x768", "768x1024", "1024x1024", "1024x1280", "1280x1280", "1280x1536", "1536x1536", "1280x720", "1280x1080", "1920x1080", "1920x1440", "2560x1440"],),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")

    FUNCTION = "resize_dimensions"

    CATEGORY = "GR85/Resolution"

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="GR85_ImageDimensionResizer",
            display_name="Image Dimension Resizer",
            category="GR85/Resolution",
            inputs=[
                io.Int.Input(
                    "original_width",
                    default=512,
                    min=1,
                    max=4096,
                ),
                io.Int.Input(
                    "original_height",
                    default=512,
                    min=1,
                    max=4096,
                ),
                io.String.Input(
                    "target_dimensions",
                    default="512x512",
                ),
            ],
            outputs=[
                io.Int.Output(),
                io.Int.Output(),
            ],
        )

    @classmethod
    def execute(
        cls,
        original_width: int,
        original_height: int,
        target_dimensions: str,
    ) -> io.NodeOutput:
        instance = cls()
        width, height = instance.resize_dimensions(
            original_width=original_width,
            original_height=original_height,
            target_dimensions=target_dimensions,
        )
        return io.NodeOutput(width, height)

    def resize_dimensions(self, original_width, original_height, target_dimensions):
        """
        Calculates new dimensions while maintaining pixel count
        and maintaining the ratio of the original dimensions.

        first calculate the original ratio
        then calculate the target pixel count
        then calculate the new dimensions
        """
        original_ratio = original_width / original_height
        target_width, target_height = map(int, target_dimensions.split("x"))
        target_pixels = target_width * target_height
        new_width = math.sqrt(target_pixels * original_ratio)
        new_height = new_width / original_ratio
        return int(round(new_width)), int(round(new_height))
