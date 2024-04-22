import math


class ImageDimensionResizer:
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
                "target_dimensions": (["512x512", "512*768", "768x768", "1024x1024", "1280x720", "1920x1080"],),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")

    FUNCTION = "resize_dimensions"

    CATEGORY = "GR85/Latent"

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
