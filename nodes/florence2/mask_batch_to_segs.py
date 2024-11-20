import numpy as np
import torch
import cv2
from collections import namedtuple
from nodes import MAX_RESOLUTION

# Helper Functions
def normalize_region(dim, start, length):
    end = int(start + length)
    if start < 0:
        start = 0
        end = int(length)
    if end > dim:
        end = dim
        start = dim - int(length)
    start = max(start, 0)
    return start, end

def make_crop_region(w, h, bbox, crop_factor, crop_min_size=None):
    x1 = bbox[0]
    y1 = bbox[1]
    x2 = bbox[2]
    y2 = bbox[3]

    bbox_w = x2 - x1
    bbox_h = y2 - y1

    crop_w = bbox_w * crop_factor
    crop_h = bbox_h * crop_factor

    if crop_min_size is not None:
        crop_w = max(crop_min_size, crop_w)
        crop_h = max(crop_min_size, crop_h)

    kernel_x = x1 + bbox_w / 2
    kernel_y = y1 + bbox_h / 2

    new_x1 = int(kernel_x - crop_w / 2)
    new_y1 = int(kernel_y - crop_h / 2)

    # Ensure position is within bounds
    new_x1, new_x2 = normalize_region(w, new_x1, crop_w)
    new_y1, new_y2 = normalize_region(h, new_y1, crop_h)

    return [new_x1, new_y1, new_x2, new_y2]

def make_2d_mask(mask):
    # Handle different mask dimensions
    if len(mask.shape) == 4:
        # Assuming mask shape is [B, H, W, C]
        if mask.shape[3] == 1:
            mask = mask[:, :, :, 0]
        else:
            mask = mask[:, :, :, 0]  # Use the first channel
    if len(mask.shape) == 3:
        # If mask is [B, H, W]
        if mask.shape[0] == 1:
            mask = mask[0]
        else:
            # Keep as is for batch processing
            pass
    return mask

# Named Tuple
SEG = namedtuple("SEG",
                 ['cropped_image', 'cropped_mask', 'confidence', 'crop_region', 'bbox', 'label', 'control_net_wrapper'],
                 defaults=[None])

# Class Definition
class MaskBatchToSEGS:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "combined": ("BOOLEAN", {"default": False, "label_on": "True", "label_off": "False"}),
                "crop_factor": ("FLOAT", {"default": 3.0, "min": 1.0, "max": 100, "step": 0.1}),
                "bbox_fill": ("BOOLEAN", {"default": False, "label_on": "enabled", "label_off": "disabled"}),
                "drop_size": ("INT", {"min": 1, "max": MAX_RESOLUTION, "step": 1, "default": 10}),
                "contour_fill": ("BOOLEAN", {"default": False, "label_on": "enabled", "label_off": "disabled"}),
            }
        }

    RETURN_TYPES = ("SEGS",)
    FUNCTION = "doit"

    CATEGORY = "GR85/Florence2"

    @staticmethod
    def mask_to_segs(mask, combined, crop_factor, bbox_fill, drop_size=1, label='A', crop_min_size=None, detailer_hook=None, is_contour=True):
        drop_size = max(drop_size, 1)
        if mask is None:
            print("[mask_to_segs] Cannot operate: MASK is empty.")
            return ([],)

        if not isinstance(mask, np.ndarray):
            try:
                mask = mask.numpy()
            except AttributeError:
                print("[mask_to_segs] Cannot operate: MASK is not a NumPy array or Tensor.")
                return ([],)

        # Ensure mask is 2D or 3D with batch dimension
        mask = make_2d_mask(mask)

        if len(mask.shape) == 2:
            mask = np.expand_dims(mask, axis=0)

        result = []

        for i in range(mask.shape[0]):
            mask_i = mask[i]

            # Ensure mask_i is 2D
            if mask_i.ndim != 2:
                print(f"[mask_to_segs] Mask at index {i} is not 2D. Shape: {mask_i.shape}")
                continue

            if np.count_nonzero(mask_i) == 0:
                print(f"[mask_to_segs] Empty mask at index {i}. Skipping.")
                continue

            if combined:
                indices = np.nonzero(mask_i)
                if len(indices[0]) > 0 and len(indices[1]) > 0:
                    bbox = (
                        np.min(indices[1]),
                        np.min(indices[0]),
                        np.max(indices[1]),
                        np.max(indices[0]),
                    )
                    crop_region = make_crop_region(mask_i.shape[1], mask_i.shape[0], bbox, crop_factor)

                    if detailer_hook:
                        crop_region = detailer_hook.post_crop_region(mask_i.shape[1], mask_i.shape[0], bbox, crop_region)

                    if crop_region[2] - crop_region[0] > 0 and crop_region[3] - crop_region[1] > 0:
                        cropped_mask = mask_i[crop_region[1]:crop_region[3], crop_region[0]:crop_region[2]]

                        if bbox_fill:
                            # Adjust bbox coordinates relative to the crop region
                            bx1, by1, bx2, by2 = bbox
                            bx1 -= crop_region[0]
                            bx2 -= crop_region[0]
                            by1 -= crop_region[1]
                            by2 -= crop_region[1]
                            cropped_mask[by1:by2, bx1:bx2] = 1.0

                        result.append(SEG(None, cropped_mask, 1.0, crop_region, bbox, label, None))
            else:
                mask_i_uint8 = (mask_i * 255.0).astype(np.uint8)

                # Debugging output
                print(f"Processing mask {i} with shape {mask_i.shape} and dtype {mask_i.dtype}")
                print(f"mask_i_uint8 shape: {mask_i_uint8.shape}, dtype: {mask_i_uint8.dtype}")

                if np.count_nonzero(mask_i_uint8) == 0:
                    print(f"[mask_to_segs] Empty mask at index {i} after conversion. Skipping.")
                    continue

                contours_info = cv2.findContours(mask_i_uint8, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                if len(contours_info) == 3:
                    contours, ctree, _ = contours_info
                else:
                    contours, ctree = contours_info

                for j, contour in enumerate(contours):
                    hierarchy = ctree[0][j]
                    if hierarchy[3] != -1:
                        continue  # Skip child contours

                    x, y, w, h = cv2.boundingRect(contour)
                    if w > drop_size and h > drop_size:
                        separated_mask = np.zeros_like(mask_i_uint8)
                        cv2.drawContours(separated_mask, [contour], -1, 255, -1)
                        separated_mask = separated_mask.astype(np.float32) / 255.0

                        bbox = x, y, x + w, y + h
                        crop_region = make_crop_region(mask_i.shape[1], mask_i.shape[0], bbox, crop_factor, crop_min_size)

                        if detailer_hook:
                            crop_region = detailer_hook.post_crop_region(mask_i.shape[1], mask_i.shape[0], bbox, crop_region)

                        cropped_mask = separated_mask[
                                       crop_region[1]:crop_region[3],
                                       crop_region[0]:crop_region[2],
                                       ]

                        if bbox_fill:
                            # Adjust bbox coordinates relative to the crop region
                            cx1, cy1, _, _ = crop_region
                            bx1 = x - cx1
                            bx2 = x + w - cx1
                            by1 = y - cy1
                            by2 = y + h - cy1
                            cropped_mask[by1:by2, bx1:bx2] = 1.0

                        result.append(SEG(None, cropped_mask, 1.0, crop_region, bbox, label, None))

        # At the end of the mask_to_segs function
        if not result:
            print(f"[mask_to_segs] No segments found.")

        print(f"# of Detected SEGS: {len(result)}")

        # Return only the result
        return result

    def doit(self, mask, combined, crop_factor, bbox_fill, drop_size=1, contour_fill=False):
        return MaskBatchToSEGS.mask_to_segs(mask, combined, crop_factor, bbox_fill, drop_size, is_contour=contour_fill)
