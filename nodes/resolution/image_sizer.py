import math
from comfy_api.latest import io


class ImageSizer(io.ComfyNode):
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "original_dimensions": (["512x512", "512x768", "768x768", "768x1024", "1024x1024", "1024x1280", "1280x1280", "1280x1536", "1536x1536", "1280x720", "1280x1080", "1920x1080", "1920x1440", "2560x1440"],),
                "width": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "height": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "orientation": (["original", "landscape", "portrait"],),
                "tolerance": ("INT", {
                    "default": 16,
                    "min": 1,
                    "max": 128,
                    "step": 1,
                    "display": "number"
                }),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")

    FUNCTION = "resize_dimensions"

    CATEGORY = "GR85/Resolution"

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="GR85_ImageSizer",
            display_name="Image Sizer",
            category="GR85/Resolution",
            inputs=[
                io.String.Input(
                    "original_dimensions",
                    default="512x512",
                ),
                io.Int.Input(
                    "width",
                    default=1,
                    min=1,
                    max=4096,
                ),
                io.Int.Input(
                    "height",
                    default=1,
                    min=1,
                    max=4096,
                ),
                io.String.Input(
                    "orientation",
                    default="original",
                ),
                io.Int.Input(
                    "tolerance",
                    default=16,
                    min=1,
                    max=128,
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
        original_dimensions: str,
        width: int,
        height: int,
        orientation: str,
        tolerance: int,
    ) -> io.NodeOutput:
        instance = cls()
        new_width, new_height = instance.resize_dimensions(
            original_dimensions=original_dimensions,
            width=width,
            height=height,
            orientation=orientation,
            tolerance=tolerance,
        )
        return io.NodeOutput(new_width, new_height)

    def resize_dimensions(self, original_dimensions, width, height, orientation, tolerance):
        source_width, source_height = map(int, original_dimensions.split("x"))

        # Total pixels in the original image
        total_pixels = source_width * source_height

        # Calculate new dimensions while maintaining the pixel count and aspect ratio
        new_height = math.sqrt(total_pixels * height / width)
        new_width = new_height * width / height

        # Adjust for orientation
        if orientation == 'landscape':
            new_width, new_height = max(new_width, new_height), min(new_width, new_height)
        elif orientation == 'portrait':
            new_width, new_height = min(new_width, new_height), max(new_width, new_height)

        # Adjust dimensions to be divisible by the tolerance value
        new_width = int(round(new_width / tolerance) * tolerance)
        new_height = int(round(new_height / tolerance) * tolerance)

        return int(new_width), int(new_height)
