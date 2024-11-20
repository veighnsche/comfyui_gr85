import torch
import torch.nn.functional as F


class FilterAndCombineMasks:
    """
    Combines masks by placing the largest first without a border.
    Smaller masks are added on top, with black borders added only if they overlap with larger masks.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "masks": ("MASK",),
                "threshold_percentage": ("FLOAT", {"default": 50.0, "min": 0.0, "max": 100.0, "step": 0.1}),
            }
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "doit"
    CATEGORY = "ImpactPack/Operation"

    def log(self, message, data=None):
        print(f"[FilterAndCombineMasks]: {message}")
        if data is not None:
            print(f"  -> Data: {data}")

    def doit(self, masks, threshold_percentage):
        self.log("Execution started.")
        if masks is None or len(masks) == 0:
            self.log("No masks provided. Returning empty mask.")
            return (torch.zeros((1, *masks[0].shape[-2:]), dtype=torch.float32),)

        # Convert masks to binary
        binary_masks = [(mask > 0).float().squeeze() for mask in masks]

        # Calculate the size threshold
        height, width = binary_masks[0].shape
        image_area = height * width
        threshold_pixels = (threshold_percentage / 100.0) * image_area

        # Filter masks by size
        valid_masks = [mask for mask in binary_masks if torch.sum(mask).item() <= threshold_pixels]
        if len(valid_masks) == 0:
            self.log("No valid masks after filtering. Returning empty mask.")
            return (torch.zeros((1, height, width), dtype=torch.float32),)

        # Sort masks by size (largest to smallest)
        valid_masks = sorted(valid_masks, key=lambda m: torch.sum(m).item(), reverse=True)

        # Initialize an empty canvas
        canvas = torch.zeros((height, width), dtype=torch.float32)
        self.log("Initialized empty canvas.")

        # Define a kernel for dilation
        border_kernel_size = 3
        kernel = torch.ones((1, 1, border_kernel_size, border_kernel_size), dtype=torch.float32)

        def add_border(mask):
            """
            Adds a black border to the given mask.
            """
            # Dilate the mask to create a border
            dilated_mask = F.conv2d(
                mask.unsqueeze(0).unsqueeze(0),
                kernel,
                padding=border_kernel_size // 2
            ).squeeze()
            dilated_mask = (dilated_mask > 0).float()

            # Extract the border by subtracting the original mask
            border = dilated_mask - mask
            border = torch.clamp(border, min=0)
            return border

        # Process each valid mask
        for i, mask in enumerate(valid_masks):
            self.log(f"Processing mask {i + 1} of {len(valid_masks)}.")
            overlap = (canvas * mask).sum().item() > 0  # Check if there is overlap
            if overlap:
                self.log(f"Mask {i + 1} overlaps with the canvas. Adding a black border.")
                border = add_border(mask)
                # Add the border to the canvas (black = 0)
                canvas = torch.where(border > 0, torch.zeros_like(canvas), canvas)
            # Add the mask itself (white = 1)
            canvas = torch.where(mask > 0, torch.ones_like(canvas), canvas)

        self.log("All masks processed successfully.")
        return (canvas.unsqueeze(0),)
