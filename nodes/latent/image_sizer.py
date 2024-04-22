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
        side_1 = math.sqrt(total_pixels * ratio_1 / ratio_2)
        side_2 = side_1 * ratio_2 / ratio_1

        bigger_side = max(side_1, side_2)
        smaller_side = min(side_1, side_2)

        if orientation == 'landscape':
            return int(round(bigger_side)), int(round(smaller_side))
        else:
            return int(round(smaller_side)), int(round(bigger_side))
