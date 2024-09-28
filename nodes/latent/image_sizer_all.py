import math

class ImageSizerAll:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pixel_amount": ("INT", {
                    "default": 1024*1024,
                    "step": 1,
                    "display": "number"
                }),
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

    FUNCTION = "resize_dimensions_all"

    CATEGORY = "GR85/Latent"

    def resize_dimensions_all(self, pixel_amount, width, height, orientation, tolerance):
        """
        Calculates new dimensions for an image while maintaining the same pixel count
        and a specified aspect ratio, adjusted to the given tolerance.

        Args:
            pixel_amount (int): The total number of pixels for the image.
            width (int): The first part of the desired aspect ratio.
            height (int): The second part of the desired aspect ratio.
            orientation (str): "original", "landscape", or "portrait".
            tolerance (int): The value to which width and height should be adjusted.

        Returns:
            tuple: A tuple containing the new width and height of the image.
        """
        # Calculate the aspect ratio based on width and height
        aspect_ratio = width / height

        # Calculate the new dimensions based on the pixel amount and aspect ratio
        new_width = math.sqrt(pixel_amount * aspect_ratio)
        new_height = new_width / aspect_ratio

        # Determine which side is bigger
        bigger_side = max(new_width, new_height)
        smaller_side = min(new_width, new_height)

        # Adjust dimensions based on orientation
        if orientation == 'original':
            final_width, final_height = int(round(new_width)), int(round(new_height))
        elif orientation == 'landscape':
            final_width, final_height = int(round(bigger_side)), int(round(smaller_side))
        elif orientation == 'portrait':
            final_width, final_height = int(round(smaller_side)), int(round(bigger_side))
        else:
            # Fallback to original if an unknown orientation is provided
            final_width, final_height = int(round(new_width)), int(round(new_height))

        # Apply tolerance by rounding to the nearest multiple of tolerance
        final_width = round(final_width / tolerance) * tolerance
        final_height = round(final_height / tolerance) * tolerance

        return final_width, final_height
