import numpy as np
import cv2
import torch
import logging

# Utility functions
def tensor_to_numpy(tensor):
    if tensor.is_cuda:
        tensor = tensor.cpu()
    return tensor.squeeze().detach().numpy()

def numpy_to_tensor(array):
    return torch.tensor(array, dtype=torch.float32)

# Gradient Rotation Transform
class RandomizedMaskTransform:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "rotation": ("FLOAT", {
                    "default": 5.0,
                    "min": -360.0,
                    "max": 360.0,
                    "step": 0.1,
                    "tooltip": "Maximum rotation angle in degrees. Set to 0 to disable rotation."
                }),
                "x_axis": ("FLOAT", {
                    "default": 0.0,
                    "min": -100.0,
                    "max": 100.0,
                    "step": 0.01,
                    "tooltip": "Shifts the center along the x-axis. -100 moves it to the left edge, 100 to the right edge."
                }),
                "y_axis": ("FLOAT", {
                    "default": 0.0,
                    "min": -100.0,
                    "max": 100.0,
                    "step": 0.01,
                    "tooltip": "Shifts the center along the y-axis. -100 moves it to the top edge, 100 to the bottom edge."
                })
            }
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "transform"

    CATEGORY = "GR85/Mask"

    def transform(self, mask, rotation, x_axis, y_axis):
        logging.info("Starting transform with center shift effect.")

        # Convert tensor to numpy
        mask = tensor_to_numpy(mask)
        h, w = mask.shape

        # Calculate new center based on x_axis and y_axis
        center_x = w / 2 + (x_axis / 100) * (w / 2)
        center_y = h / 2 + (y_axis / 100) * (h / 2)

        logging.debug(f"Mask dimensions: {w}x{h}, New Center: ({center_x}, {center_y})")

        # Create normalized distance map from the new center
        y_indices, x_indices = np.ogrid[:h, :w]
        distances = np.sqrt((x_indices - center_x) ** 2 + (y_indices - center_y) ** 2)
        max_distance = np.sqrt((max(center_x, w - center_x)) ** 2 + (max(center_y, h - center_y)) ** 2)
        normalized_distances = distances / max_distance

        logging.debug("Normalized distance map calculated.")

        # If rotation is 0, return mask with adjusted center
        if rotation == 0:
            logging.info("Rotation is 0; applying center shift without rotation.")
            return (numpy_to_tensor(mask),)

        # Calculate per-pixel rotation angles based on the distance map
        per_pixel_rotation = rotation * (1 - normalized_distances)

        # Create coordinate grids
        coords_x, coords_y = np.meshgrid(np.arange(w), np.arange(h))

        # Calculate rotated coordinates using per-pixel rotation
        angle_map = np.deg2rad(per_pixel_rotation)
        delta_x = coords_x - center_x
        delta_y = coords_y - center_y

        rotated_x = center_x + delta_x * np.cos(angle_map) - delta_y * np.sin(angle_map)
        rotated_y = center_y + delta_x * np.sin(angle_map) + delta_y * np.cos(angle_map)

        logging.debug("Per-pixel rotation grid calculated.")

        # Map rotated coordinates back to mask
        rotated_mask = cv2.remap(
            mask,
            rotated_x.astype(np.float32),
            rotated_y.astype(np.float32),
            interpolation=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=0,
        )

        logging.info("Gradient rotation with center shift applied successfully.")

        # Convert back to tensor
        output_tensor = numpy_to_tensor(rotated_mask)
        return (output_tensor,)

