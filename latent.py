import math


class ImageSizer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "original_dimensions": (["512x512", "512*768", "768x768", "1024x1024", "1280x720", "1920x1080"],),
                "ratio_1": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "ratio_2": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "orientation": (["landscape", "portrait"],),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")

    FUNCTION = "resize_dimensions"

    CATEGORY = "GR85/Latent"

    def resize_dimensions(self, original_dimensions, ratio_1, ratio_2, orientation):
        original_width, original_height = map(int, original_dimensions.split("x"))

        """Calculates new dimensions for an image while maintaining the same pixel count
          and a specified aspect ratio.
         
        Args:
          original_width: The original width of the image in pixels.
          original_height: The original height of the image in pixels.
          ratio_1: The first part of the desired aspect ratio.
          ratio_2: The second part of the desired aspect ratio.
          orientation: Either "landscape" or "portrait" (used for clarity, not calculation)
         
        Returns:
          A tuple containing the new width and height of the image.
        """

        total_pixels = original_width * original_height
        new_width = math.sqrt(total_pixels * ratio_1 / ratio_2)
        new_height = new_width * ratio_2 / ratio_1

        # Adjust if the desired orientation is different from the original
        if (orientation == 'landscape' and original_height > original_width) or \
                (orientation == 'portrait' and original_width > original_height):
            new_width, new_height = new_height, new_width  # Swap dimensions

        return int(round(new_width)), int(round(new_height))


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
