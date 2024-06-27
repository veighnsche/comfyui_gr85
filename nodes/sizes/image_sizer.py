import math

class ImageSizer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "original_dimensions": (["512x512", "512x768", "768x768", "768x1024", "1024x1024", "1280x720", "1280x1080", "1920x1080", "1920x1440", "2560x1440"],),
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
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")

    FUNCTION = "resize_dimensions"

    CATEGORY = "GR85/Sizes"

    def resize_dimensions(self, original_dimensions, width, height):
        original_width, original_height = map(int, original_dimensions.split("x"))

        """Calculates new dimensions for an image while maintaining the same pixel count
          and a specified aspect ratio.
         
        Args:
          original_width: The original width of the image in pixels.
          original_height: The original height of the image in pixels.
          width: The desired width for the new aspect ratio.
          height: The desired height for the new aspect ratio.
         
        Returns:
          A tuple containing the new width and height of the image.
        """

        total_pixels = original_width * original_height
        side_1 = math.sqrt(total_pixels * width / height)
        side_2 = side_1 * height / width

        new_width = int(round(side_1))
        new_height = int(round(side_2))

        return new_width, new_height