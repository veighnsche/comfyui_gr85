import torch
import torchvision.transforms.functional as TF


def tensor2rgb(t: torch.Tensor) -> torch.Tensor:
    size = t.size()
    if (len(size) < 4):
        return t.unsqueeze(3).repeat(1, 1, 1, 3)
    if size[3] == 1:
        return t.repeat(1, 1, 1, 3)
    elif size[3] == 4:
        return t[:, :, :, :3]
    else:
        return t


def tensor2rgba(t: torch.Tensor) -> torch.Tensor:
    size = t.size()
    if (len(size) < 4):
        return t.unsqueeze(3).repeat(1, 1, 1, 4)
    elif size[3] == 1:
        return t.repeat(1, 1, 1, 4)
    elif size[3] == 3:
        alpha_tensor = torch.ones((size[0], size[1], size[2], 1))
        return torch.cat((t, alpha_tensor), dim=3)
    else:
        return t


def tensor2mask(t: torch.Tensor) -> torch.Tensor:
    size = t.size()
    if (len(size) < 4):
        return t
    if size[3] == 1:
        return t[:, :, :, 0]
    elif size[3] == 4:
        # Not sure what the right thing to do here is. Going to try to be a little smart and use alpha unless all alpha is 1 in case we'll fallback to RGB behavior
        if torch.min(t[:, :, :, 3]).item() != 1.:
            return t[:, :, :, 3]

    return TF.rgb_to_grayscale(tensor2rgb(t).permute(0, 3, 1, 2), num_output_channels=1)[:, 0, :, :]


class PasteByMaskGr85:
    """
    Pastes `image_to_paste` onto `image_base` using `mask` to determine the location. The `resize_behavior` parameter determines how the image to paste is resized to fit the mask. If `mask_mapping_optional` obtained from a 'Separate Mask Components' node is used, it will control which image gets pasted onto which base image.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_base": ("IMAGE",),
                "image_to_paste": ("IMAGE",),
                "mask": ("IMAGE",),
                "resize_behavior": ([
                                        "resize",
                                        "keep_ratio_fill",
                                        "keep_ratio_fit",
                                        "source_size",
                                        "source_size_unmasked",
                                        "keep_ratio_unmasked"  # Added new option here
                                    ],)
            },
            "optional": {
                "mask_mapping_optional": ("MASK_MAPPING",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "paste"

    CATEGORY = "GR85/Mask"

    def paste(self, image_base, image_to_paste, mask, resize_behavior, mask_mapping_optional=None):
        import torch
        import math
        from torchvision.ops import masks_to_boxes

        # Convert tensors to appropriate formats
        image_base = tensor2rgba(image_base)
        image_to_paste = tensor2rgba(image_to_paste)
        mask = tensor2mask(mask)

        # Ensure mask matches the size of the base image
        B, H, W, C = image_base.shape
        MB = mask.shape[0]
        PB = image_to_paste.shape[0]

        if mask_mapping_optional is None:
            if B < PB:
                assert PB % B == 0, "Batch size of image_to_paste must be a multiple of image_base batch size."
                image_base = image_base.repeat(PB // B, 1, 1, 1)
            B, H, W, C = image_base.shape
            if MB < B:
                assert B % MB == 0, "Batch size of mask must divide evenly into image_base batch size."
                mask = mask.repeat(B // MB, 1, 1)
            elif B < MB:
                assert MB % B == 0, "Batch size of image_base must divide evenly into mask batch size."
                image_base = image_base.repeat(MB // B, 1, 1, 1)
            if PB < B:
                assert B % PB == 0, "Batch size of image_to_paste must divide evenly into image_base batch size."
                image_to_paste = image_to_paste.repeat(B // PB, 1, 1, 1)

        # Resize mask to match base image dimensions
        mask = torch.nn.functional.interpolate(mask.unsqueeze(1), size=(H, W), mode='nearest')[:, 0, :, :]
        MB, MH, MW = mask.shape

        # Handle empty masks
        is_empty = ~torch.gt(torch.max(torch.reshape(mask, [MB, MH * MW]), dim=1).values, 0.)
        mask[is_empty, 0, 0] = 1.
        boxes = masks_to_boxes(mask)
        mask[is_empty, 0, 0] = 0.

        min_x = boxes[:, 0]
        min_y = boxes[:, 1]
        max_x = boxes[:, 2]
        max_y = boxes[:, 3]
        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2

        target_width = max_x - min_x + 1
        target_height = max_y - min_y + 1

        result = image_base.detach().clone()
        for i in range(0, MB):
            if is_empty[i]:
                continue
            else:
                image_index = i
                if mask_mapping_optional is not None:
                    image_index = mask_mapping_optional[i].item()
                source_size = image_to_paste.size()
                SB, SH, SW, _ = image_to_paste.shape

                # Determine desired size based on resize_behavior
                width = int(target_width[i].item())
                height = int(target_height[i].item())

                if resize_behavior == "keep_ratio_fill":
                    target_ratio = width / height
                    actual_ratio = SW / SH
                    if actual_ratio > target_ratio:
                        width = int(height * actual_ratio)
                    elif actual_ratio < target_ratio:
                        height = int(width / actual_ratio)
                elif resize_behavior == "keep_ratio_fit":
                    target_ratio = width / height
                    actual_ratio = SW / SH
                    if actual_ratio > target_ratio:
                        height = int(width / actual_ratio)
                    elif actual_ratio < target_ratio:
                        width = int(height * actual_ratio)
                elif resize_behavior == "source_size" or resize_behavior == "source_size_unmasked":
                    width = SW
                    height = SH
                elif resize_behavior == "keep_ratio_unmasked":
                    # New behavior implementation
                    actual_ratio = SW / SH
                    # Resize image to fit within mask dimensions while preserving aspect ratio
                    if SW > width or SH > height:
                        scale_factor = min(width / SW, height / SH)
                        width = int(SW * scale_factor)
                        height = int(SH * scale_factor)
                    else:
                        width = SW
                        height = SH

                # Resize the image_to_paste if needed
                resized_image = image_to_paste[i].unsqueeze(0)
                if SH != height or SW != width:
                    resized_image = torch.nn.functional.interpolate(
                        resized_image.permute(0, 3, 1, 2),
                        size=(height, width),
                        mode='bicubic',
                        align_corners=False
                    ).permute(0, 2, 3, 1)

                pasting = torch.ones([H, W, C], device=resized_image.device)
                ymid = float(mid_y[i].item())
                xmid = float(mid_x[i].item())
                ymin = int(math.floor(ymid - height / 2))
                ymax = ymin + height
                xmin = int(math.floor(xmid - width / 2))
                xmax = xmin + width

                # Adjust source and target coordinates for boundaries
                source_ymin, source_xmin = 0, 0
                source_ymax, source_xmax = height, width

                if xmin < 0:
                    source_xmin = -xmin
                    xmin = 0
                if ymin < 0:
                    source_ymin = -ymin
                    ymin = 0
                if xmax > W:
                    source_xmax -= (xmax - W)
                    xmax = W
                if ymax > H:
                    source_ymax -= (ymax - H)
                    ymax = H

                # Paste the resized image onto the base image
                pasting[ymin:ymax, xmin:xmax, :] = resized_image[0, source_ymin:source_ymax, source_xmin:source_xmax, :]
                pasting_alpha = torch.zeros([H, W], device=resized_image.device)
                pasting_alpha[ymin:ymax, xmin:xmax] = resized_image[0, source_ymin:source_ymax, source_xmin:source_xmax,
                                                      3]

                if resize_behavior in ["keep_ratio_fill", "source_size_unmasked", "keep_ratio_unmasked"]:
                    # Allow the image to extend outside the mask area
                    paste_mask = pasting_alpha.unsqueeze(2).repeat(1, 1, 4)
                else:
                    paste_mask = torch.min(pasting_alpha, mask[i]).unsqueeze(2).repeat(1, 1, 4)

                result[image_index] = pasting * paste_mask + result[image_index] * (1. - paste_mask)

        return (result,)
