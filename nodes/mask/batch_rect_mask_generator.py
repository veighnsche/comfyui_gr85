import torch

VERY_BIG_SIZE = 1024 * 1024

class BatchRectMaskGenerator:
    """
    Creates rectangle masks. If copy_image_size is provided, the image_width and image_height parameters are ignored,
    and the size of the given image will be used instead.
    The 'y' input can now be a list of strings representing y-coordinates for multiple masks.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (["percent", "pixels"],),
                "origin": (["topleft", "bottomleft", "topright", "bottomright"],),
                "x": ("FLOAT", {"default": 0, "min": 0, "max": VERY_BIG_SIZE, "step": 1}),
                "y": ("LIST", {"default": ["0"]}),  # List of strings
                "width": ("FLOAT", {"default": 50, "min": 0, "max": VERY_BIG_SIZE, "step": 1}),
                "height": ("FLOAT", {"default": 50, "min": 0, "max": VERY_BIG_SIZE, "step": 1}),
                "image_width": ("INT", {"default": 512, "min": 64, "max": VERY_BIG_SIZE, "step": 64}),
                "image_height": ("INT", {"default": 512, "min": 64, "max": VERY_BIG_SIZE, "step": 64}),
            },
            "optional": {
                "copy_image_size": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    OUTPUT_IS_LIST = (True,)

    FUNCTION = "create_mask"

    CATEGORY = "Masquerade Nodes"

    def create_mask(self, mode, origin, x, y, width, height, image_width, image_height, copy_image_size=None):
        # Convert y values from list of strings to a tensor of floats
        y_values = torch.tensor([float(val) for val in y])

        if copy_image_size is not None:
            size = copy_image_size.size()
            image_width = size[2]
            image_height = size[1]

        # Create tensors for x, width, and height
        x_tensor = torch.tensor([x])
        width_tensor = torch.tensor([width])
        height_tensor = torch.tensor([height])

        # Adjust for 'percent' mode
        if mode == "percent":
            x_tensor = x_tensor / 100.0 * image_width
            y_values = y_values / 100.0 * image_height
            width_tensor = width_tensor / 100.0 * image_width
            height_tensor = height_tensor / 100.0 * image_height

        # Compute min_x and max_x
        min_x = x_tensor
        max_x = min_x + width_tensor

        # Adjust x-values based on the origin
        if origin in ("topright", "bottomright"):
            min_x, max_x = image_width - max_x, image_width - min_x

        # Clamp x indices
        min_x = min_x.clamp(0, image_width)
        max_x = max_x.clamp(0, image_width)

        # Compute min_y and max_y
        min_y = y_values
        max_y = min_y + height_tensor

        # Adjust y-values based on the origin
        if origin in ("bottomleft", "bottomright"):
            min_y, max_y = image_height - max_y, image_height - min_y

        # Clamp y indices
        min_y = min_y.clamp(0, image_height)
        max_y = max_y.clamp(0, image_height)

        # Ensure min <= max
        min_x, max_x = torch.min(min_x, max_x), torch.max(min_x, max_x)
        min_y, max_y = torch.min(min_y, max_y), torch.max(min_y, max_y)

        # Convert indices to integers
        min_x = min_x.long()
        max_x = max_x.long()
        min_y = min_y.long()
        max_y = max_y.long()

        # Create an empty masks tensor
        num_masks = y_values.size(0)
        masks = torch.zeros((num_masks, image_height, image_width))

        # Generate grid indices
        for i in range(num_masks):
            masks[i, min_y[i]:max_y[i], min_x[0]:max_x[0]] = 1

        # Return the list of masks with channel dimension added
        return ([mask.unsqueeze(0) for mask in masks],)
