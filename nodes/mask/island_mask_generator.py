import torch
import numpy as np

# Utility functions
def to_numpy(tensor):
    if tensor.is_cuda:
        tensor = tensor.cpu()
    return tensor.squeeze().detach().numpy()

def to_tensor(array):
    return torch.tensor(array, dtype=torch.float32)

class IslandMaskGenerator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "processed_mask": ("MASK", {"label": "Processed Mask"}),
                "grid_size": ("INT", {"default": 128, "min": 16, "max": 512, "step": 16}),
                "border_thickness": ("INT", {"default": 4, "min": 1, "max": 32, "step": 1}),
            },
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("island_mask",)
    FUNCTION = "generate_island_mask"
    CATEGORY = "GR85/Mask"

    @staticmethod
    def generate_island_mask(processed_mask, grid_size, border_thickness):
        # Convert processed_mask to PyTorch tensor if it is a NumPy array
        if isinstance(processed_mask, np.ndarray):
            processed_mask = torch.tensor(processed_mask, dtype=torch.float32)

        # Ensure processed_mask is in 4D format (B, C, H, W)
        if processed_mask.ndim == 2:  # Single 2D mask
            processed_mask = processed_mask.unsqueeze(0).unsqueeze(0)
        elif processed_mask.ndim == 3:  # Single mask with channel
            processed_mask = processed_mask.unsqueeze(0)
        elif processed_mask.ndim != 4:
            raise ValueError(f"Expected 2D, 3D, or 4D processed mask. Got shape: {processed_mask.shape}")

        # Create island_mask based on grid size and input mask
        _, _, height, width = processed_mask.shape
        island_mask = torch.zeros_like(processed_mask, dtype=torch.uint8)

        for y in range(0, height, grid_size):
            for x in range(0, width, grid_size):
                x_end = min(x + grid_size, width)
                y_end = min(y + grid_size, height)

                # Define inner region (excludes borders)
                inner_y_start = y + border_thickness
                inner_y_end = max(y_end - border_thickness, y)
                inner_x_start = x + border_thickness
                inner_x_end = max(x_end - border_thickness, x)

                # Extract the corresponding inner region from the processed_mask
                if inner_y_start < inner_y_end and inner_x_start < inner_x_end:
                    region = processed_mask[:, :, inner_y_start:inner_y_end, inner_x_start:inner_x_end]
                    island_mask[:, :, inner_y_start:inner_y_end, inner_x_start:inner_x_end] = (region > 0).byte()

        return island_mask
