import numpy as np
import torch
import cv2


class MaskSplitter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_mask": ("MASK", {"label": "Input Mask"}),
                "size_threshold": ("INT", {"default": 128, "min": 32, "max": 512, "step": 32}),
            },
        }

    RETURN_TYPES = ("MASK", "BBOX")
    RETURN_NAMES = ("processed_masks", "bbox_metadata")
    FUNCTION = "split_mask"
    CATEGORY = "GR85/Mask"

    @staticmethod
    def split_mask(input_mask, size_threshold):
        """
        Split a binary mask into disjoint regions and further split large regions into smaller segments if necessary.
        """
        print(f"Starting mask splitting with size threshold: {size_threshold}")

        # Preprocess mask
        input_mask = MaskSplitter._preprocess_mask(input_mask)

        # Detect connected components
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(input_mask, connectivity=8)
        print(f"Total connected components (excluding background): {num_labels - 1}")

        # Process labels
        processed_masks, bbox_metadata = MaskSplitter._process_labels(labels, stats, num_labels, size_threshold)

        # Combine all processed masks
        combined_mask = MaskSplitter._combine_masks(processed_masks, input_mask.shape)
        combined_mask = torch.as_tensor(combined_mask, dtype=torch.float32)

        print(f"Mask splitting complete. Total bounding boxes generated: {len(bbox_metadata)}")
        return combined_mask, bbox_metadata

    @staticmethod
    def _preprocess_mask(input_mask):
        """
        Convert input mask to a binary NumPy array.
        """
        print("Preprocessing the input mask...")
        if isinstance(input_mask, torch.Tensor):
            input_mask = input_mask.cpu().numpy()

        input_mask = np.squeeze(input_mask)
        input_mask = np.where(input_mask > 0, 255, 0).astype(np.uint8)

        print(f"Input mask preprocessing complete. Shape: {input_mask.shape}, dtype: {input_mask.dtype}, "
              f"non-zero pixel count: {np.count_nonzero(input_mask)}")
        return input_mask

    @staticmethod
    def _process_labels(labels, stats, num_labels, size_threshold):
        """
        Process connected components, splitting large regions as needed.
        """
        processed_masks = []
        bbox_metadata = []

        for label in range(1, num_labels):  # Skip background
            x, y, w, h, area = stats[label]
            region_mask = (labels == label).astype(np.uint8) * 255

            print(f"Processing label {label}: x={x}, y={y}, w={w}, h={h}, area={area}")
            if w > size_threshold or h > size_threshold:
                print(f"Label {label} exceeds size threshold. Splitting...")
                sub_masks, sub_bboxes = MaskSplitter._split_large_region(region_mask, x, y, w, h, size_threshold)
                processed_masks.extend(sub_masks)
                bbox_metadata.extend(sub_bboxes)
            else:
                processed_masks.append(region_mask)
                bbox_metadata.append((x, y, x + w, y + h))

        print(f"Total processed masks: {len(processed_masks)}")
        return processed_masks, bbox_metadata

    @staticmethod
    def _split_large_region(region_mask, x, y, w, h, size_threshold):
        """
        Split a large region into smaller sub-regions.
        """
        sub_masks = []
        sub_bboxes = []
        step_x = min(size_threshold, w)
        step_y = min(size_threshold, h)

        for i in range(0, h, step_y):
            for j in range(0, w, step_x):
                sub_x_start = j
                sub_x_end = min(j + step_x, w)
                sub_y_start = i
                sub_y_end = min(i + step_y, h)

                sub_mask = np.zeros_like(region_mask)
                sub_mask[sub_y_start:sub_y_end, sub_x_start:sub_x_end] = \
                    region_mask[sub_y_start:sub_y_end, sub_x_start:sub_x_end]

                if np.any(sub_mask):
                    sub_masks.append(sub_mask)
                    sub_bboxes.append((x + sub_x_start, y + sub_y_start, x + sub_x_end, y + sub_y_end))
                else:
                    print(f"Skipped empty sub-region at x_start={sub_x_start}, y_start={sub_y_start}, "
                          f"x_end={sub_x_end}, y_end={sub_y_end}")

        print(f"Total sub-regions created: {len(sub_masks)}")
        return sub_masks, sub_bboxes

    @staticmethod
    def _combine_masks(masks, shape):
        """
        Combine multiple binary masks into a single mask.
        """
        combined_mask = np.zeros(shape, dtype=np.uint8)
        for mask in masks:
            combined_mask = np.maximum(combined_mask, mask)
        print("Combining complete.")
        return combined_mask
