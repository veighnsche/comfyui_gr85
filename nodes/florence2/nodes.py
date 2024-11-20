import os
import re
import math
from typing import List, Tuple

import matplotlib
import torchvision.transforms.functional as F

matplotlib.use('Agg')

script_directory = os.path.dirname(os.path.abspath(__file__))
import torch
import torch.nn.functional as F
import numpy as np
import json
import random
import hashlib
import io
from PIL import Image, ImageDraw, ImageFont, ImageColor
from matplotlib import pyplot as plt
from matplotlib import patches
import torchvision.transforms.functional as TF

from contextlib import nullcontext

import comfy.model_management as mm
from comfy.utils import ProgressBar, common_upscale

class Florence2RunCTPG:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", ),
                "florence2_model": ("FL2MODEL", ),
                "text_input": ("STRING", {"default": "", "multiline": True}),
                "fill_mask": ("BOOLEAN", {"default": True}),
                "combine_masks": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "keep_model_loaded": ("BOOLEAN", {"default": False}),
                "max_new_tokens": ("INT", {"default": 1024, "min": 1, "max": 4096}),
                "num_beams": ("INT", {"default": 3, "min": 1, "max": 64}),
                "do_sample": ("BOOLEAN", {"default": True}),
                "output_mask_select": ("STRING", {"default": ""}),
                "seed": ("INT", {"default": 1, "min": 1, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "JSON")
    RETURN_NAMES = ("image", "mask", "caption", "data")
    FUNCTION = "encode"
    CATEGORY = "GR85/Florence2"

    def hash_seed(self, seed):
        # Convert the seed to a string and then to bytes
        seed_bytes = str(seed).encode('utf-8')
        # Create a SHA-256 hash of the seed bytes
        hash_object = hashlib.sha256(seed_bytes)
        # Convert the hash to an integer
        hashed_seed = int(hash_object.hexdigest(), 16)
        # Ensure the hashed seed is within the acceptable range for set_seed
        return hashed_seed % (2**32)

    def set_seed(self, seed):
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)
        torch.backends.cudnn.deterministic = True

    def encode(self, image, text_input, florence2_model, fill_mask, combine_masks=True, keep_model_loaded=False,
               num_beams=3, max_new_tokens=1024, do_sample=True, output_mask_select="", seed=None):
        device = mm.get_torch_device()
        _, height, width, _ = image.shape
        offload_device = mm.unet_offload_device()
        annotated_image_tensor = None
        mask_tensor = None
        processor = florence2_model['processor']
        model = florence2_model['model']
        dtype = florence2_model['dtype']
        model.to(device)

        if seed:
            self.set_seed(self.hash_seed(seed))

        colormap = ['blue','orange','green','purple','brown','pink','olive','cyan','red',
                    'lime','indigo','violet','aqua','magenta','gold','tan','skyblue']

        task_prompt = '<CAPTION_TO_PHRASE_GROUNDING>'

        if text_input != "":
            prompt = task_prompt + " " + text_input
        else:
            prompt = task_prompt

        image = image.permute(0, 3, 1, 2)

        out = []
        out_masks = []
        out_results = []
        out_data = []
        pbar = ProgressBar(len(image))
        for img in image:
            image_pil = TF.to_pil_image(img)
            inputs = processor(text=prompt, images=image_pil, return_tensors="pt", do_rescale=False).to(dtype).to(device)

            generated_ids = model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                num_beams=num_beams,
            )

            results = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
            print(results)
            # Clean up the special tokens from the final list
            clean_results = results.replace('</s>', '').replace('<s>', '')

            # Return single string if only one image for compatibility with nodes that can't handle string lists
            if len(image) == 1:
                out_results = clean_results
            else:
                out_results.append(clean_results)

            W, H = image_pil.size

            parsed_answer = processor.post_process_generation(results, task=task_prompt, image_size=(W, H))

            # Process 'caption_to_phrase_grounding' task
            fig, ax = plt.subplots(figsize=(W / 100, H / 100), dpi=100)
            fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
            ax.imshow(image_pil)
            bboxes = parsed_answer[task_prompt]['bboxes']
            labels = parsed_answer[task_prompt]['labels']

            mask_indexes = []
            # Determine mask indexes outside the loop
            if output_mask_select != "":
                mask_indexes = [n.strip() for n in output_mask_select.split(",")]
                print("Mask indexes:", mask_indexes)
            else:
                mask_indexes = [str(i) for i in range(len(bboxes))]

            # Initialize mask layers
            if fill_mask:
                if combine_masks:
                    mask_layer = Image.new('RGB', image_pil.size, (0, 0, 0))
                    mask_draw = ImageDraw.Draw(mask_layer)
                else:
                    mask_layers = [Image.new('RGB', image_pil.size, (0, 0, 0)) for _ in bboxes]

            for index, (bbox, label) in enumerate(zip(bboxes, labels)):
                # Modify the label to include the index
                indexed_label = f"{index}.{label}"

                if fill_mask:
                    if str(index) in mask_indexes or label in mask_indexes:
                        print("Match index:", str(index), "in mask_indexes:", mask_indexes)
                        if combine_masks:
                            mask_draw.rectangle([bbox[0], bbox[1], bbox[2], bbox[3]], fill=(255, 255, 255))
                        else:
                            mask_draw_individual = ImageDraw.Draw(mask_layers[index])
                            mask_draw_individual.rectangle([bbox[0], bbox[1], bbox[2], bbox[3]], fill=(255, 255, 255))
                # Create a Rectangle patch
                rect = patches.Rectangle(
                    (bbox[0], bbox[1]),  # (x,y) - lower left corner
                    bbox[2] - bbox[0],   # Width
                    bbox[3] - bbox[1],   # Height
                    linewidth=1,
                    edgecolor='r',
                    facecolor='none',
                    label=indexed_label
                )
                # Calculate text width with a rough estimation
                text_width = len(label) * 6  # Adjust multiplier based on your font size
                text_height = 12  # Adjust based on your font size

                # Initial text position
                text_x = bbox[0]
                text_y = bbox[1] - text_height  # Position text above the top-left of the bbox

                # Adjust text_x if text is going off the left or right edge
                if text_x < 0:
                    text_x = 0
                elif text_x + text_width > W:
                    text_x = W - text_width

                # Adjust text_y if text is going off the top edge
                if text_y < 0:
                    text_y = bbox[3]  # Move text below the bottom-left of the bbox if it doesn't overlap with bbox

                # Add the rectangle to the plot
                ax.add_patch(rect)
                facecolor = random.choice(colormap)
                # Add the label
                plt.text(
                    text_x,
                    text_y,
                    indexed_label,
                    color='white',
                    fontsize=12,
                    bbox=dict(facecolor=facecolor, alpha=0.5)
                )
            if fill_mask:
                if combine_masks:
                    mask_tensor = TF.to_tensor(mask_layer)
                    mask_tensor = mask_tensor.unsqueeze(0).permute(0, 2, 3, 1).cpu().float()
                    mask_tensor = mask_tensor.mean(dim=0, keepdim=True)
                    mask_tensor = mask_tensor.repeat(1, 1, 1, 3)
                    mask_tensor = mask_tensor[:, :, :, 0]
                    out_masks.append(mask_tensor)
                else:
                    # Create mask tensors for each individual mask and stack them into a batch tensor
                    mask_tensors = []
                    for mask_img in mask_layers:
                        mask_tensor = TF.to_tensor(mask_img)
                        mask_tensor = mask_tensor.unsqueeze(0).permute(0, 2, 3, 1).cpu().float()
                        mask_tensor = mask_tensor.mean(dim=0, keepdim=True)
                        mask_tensor = mask_tensor.repeat(1, 1, 1, 3)
                        mask_tensor = mask_tensor[:, :, :, 0]
                        mask_tensors.append(mask_tensor)
                    if mask_tensors:
                        out_mask_tensor = torch.stack(mask_tensors, dim=0)  # Shape: (num_masks, H, W)
                        out_masks.append(out_mask_tensor)
                    else:
                        out_mask_tensor = torch.zeros((1, 64, 64), dtype=torch.float32, device="cpu")
                        out_masks.append(out_mask_tensor)

            # Remove axis and padding around the image
            ax.axis('off')
            ax.margins(0,0)
            ax.get_xaxis().set_major_locator(plt.NullLocator())
            ax.get_yaxis().set_major_locator(plt.NullLocator())
            fig.canvas.draw()
            buf = io.BytesIO()
            plt.savefig(buf, format='png', pad_inches=0)
            buf.seek(0)
            annotated_image_pil = Image.open(buf)

            annotated_image_tensor = TF.to_tensor(annotated_image_pil)
            out_tensor = annotated_image_tensor[:3, :, :].unsqueeze(0).permute(0, 2, 3, 1).cpu().float()
            out.append(out_tensor)

            out_data.append(bboxes)

            pbar.update(1)
            plt.close(fig)

        if len(out) > 0:
            out_tensor = torch.cat(out, dim=0)
        else:
            out_tensor = torch.zeros((1, 64, 64, 3), dtype=torch.float32, device="cpu")

        if not fill_mask:
            out_mask_tensor = torch.zeros((1, 64, 64), dtype=torch.float32, device="cpu")
        else:
            if combine_masks:
                if len(out_masks) > 0:
                    out_mask_tensor = torch.cat(out_masks, dim=0)  # Combined or batch tensor
                else:
                    out_mask_tensor = torch.zeros((1, 64, 64), dtype=torch.float32, device="cpu")
            else:
                if len(out_masks) > 0:
                    out_mask_tensor = out_masks[0]  # Single batch tensor
                else:
                    out_mask_tensor = torch.zeros((1, 64, 64), dtype=torch.float32, device="cpu")

        if not keep_model_loaded:
            print("Offloading model...")
            model.to(offload_device)
            mm.soft_empty_cache()

        return (out_tensor, out_mask_tensor, out_results, out_data)


class Sam2Segmentation:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sam2_model": ("SAM2MODEL",),
                "image": ("IMAGE",),
                "keep_model_loaded": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "coordinates_positive": ("STRING", {"forceInput": True}),
                "coordinates_negative": ("STRING", {"forceInput": True}),
                "bboxes": ("BBOX",),
                "individual_objects": ("BOOLEAN", {"default": False}),
                "mask": ("MASK",),
                "combine": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "segment"
    CATEGORY = "GR85/Florence2"

    def segment(self, image, sam2_model, keep_model_loaded, coordinates_positive=None, coordinates_negative=None,
                individual_objects=False, bboxes=None, mask=None, combine=True):
        offload_device = mm.unet_offload_device()
        model = sam2_model["model"]
        device = sam2_model["device"]
        dtype = sam2_model["dtype"]
        segmentor = sam2_model["segmentor"]
        B, H, W, C = image.shape

        # Handle mask input: can be a tensor or a list of tensors
        if mask is not None:
            if isinstance(mask, list):
                # Ensure all masks are tensors and stack them into a batch tensor
                mask_tensor = torch.stack(mask, dim=0).unsqueeze(1)  # [N, 1, H, W]
            else:
                # Single mask tensor [H, W]
                mask_tensor = mask.clone().unsqueeze(0).unsqueeze(1)  # [1, 1, H, W]
            # Interpolate mask to desired size
            mask_tensor = F.interpolate(mask_tensor, size=(256, 256), mode="bilinear", align_corners=False)
            # Remove channel dimension if necessary
            mask_tensor = mask_tensor.squeeze(1)  # [N, 256, 256]
        else:
            mask_tensor = None

        # Validate segmentor type
        if segmentor == 'automaskgenerator':
            raise ValueError("For automaskgenerator use Sam2AutoMaskSegmentation node")
        if segmentor == 'single_image' and B > 1:
            print("Segmenting batch of images with single_image segmentor")
        if segmentor == 'video' and bboxes is not None and "2.1" not in sam2_model["version"]:
            raise ValueError("2.0 model doesn't support bboxes with video segmentor")
        if segmentor == 'video':
            model_input_image_size = model.image_size
            print("Resizing to model input image size:", model_input_image_size)
            image = mm.common_upscale(image.movedim(-1, 1), model_input_image_size, model_input_image_size, "bilinear", "disabled").movedim(1, -1)

        # Handle point coordinates
        if coordinates_positive is not None:
            try:
                coordinates_positive = json.loads(coordinates_positive.replace("'", '"'))
                coordinates_positive = [(coord['x'], coord['y']) for coord in coordinates_positive]
                if coordinates_negative is not None:
                    coordinates_negative = json.loads(coordinates_negative.replace("'", '"'))
                    coordinates_negative = [(coord['x'], coord['y']) for coord in coordinates_negative]
            except json.JSONDecodeError as e:
                print("JSON Decode Error:", e)
                coordinates_positive = None
                coordinates_negative = None

            if not individual_objects:
                positive_point_coords = np.atleast_2d(np.array(coordinates_positive))
            else:
                positive_point_coords = np.array([np.atleast_2d(coord) for coord in coordinates_positive])

            if coordinates_negative is not None:
                negative_point_coords = np.array(coordinates_negative)
                if individual_objects:
                    while negative_point_coords.shape[0] < positive_point_coords.shape[0]:
                        negative_point_coords = np.concatenate((negative_point_coords, negative_point_coords[:1, :, :]), axis=0)
                    final_coords = np.concatenate((positive_point_coords, negative_point_coords), axis=1)
                else:
                    final_coords = np.concatenate((positive_point_coords, negative_point_coords), axis=0)
            else:
                final_coords = positive_point_coords
        else:
            final_coords = None

        # Handle bounding boxes
        if bboxes is not None:
            boxes_np_batch = [np.array(bbox_list) for bbox_list in bboxes]
            final_box = np.array(boxes_np_batch) if individual_objects else np.array(boxes_np_batch[0])
        else:
            final_box = None

        # Handle labels
        if final_coords is not None:
            positive_point_labels = np.ones(len(positive_point_coords)) if not individual_objects else np.array([[1]] * len(positive_point_coords))
            if coordinates_negative is not None:
                negative_point_labels = np.zeros(len(negative_point_coords)) if not individual_objects else np.array([[0]] * len(negative_point_coords))
                final_labels = np.concatenate((positive_point_labels, negative_point_labels),
                                              axis=0 if not individual_objects else 1)
            else:
                final_labels = positive_point_labels
        else:
            final_labels = None

        try:
            model.to(device)
        except Exception as e:
            print("Error moving model to device:", e)
            model.model.to(device)

        autocast_condition = not mm.is_device_mps(device)
        with torch.autocast(mm.get_autocast_device(device), dtype=dtype) if autocast_condition else nullcontext():
            if segmentor == 'single_image':
                image_np = (image.contiguous() * 255).byte().numpy()
                out_masks = []
                for img_np in image_np:
                    model.set_image(img_np)
                    input_box = final_box if bboxes is not None else None

                    out_masks_np, scores, logits = model.predict(
                        point_coords=final_coords if final_coords is not None else None,
                        point_labels=final_labels if final_labels is not None else None,
                        box=input_box,
                        multimask_output=True if not individual_objects else False,
                        mask_input=mask_tensor.unsqueeze(0) if mask_tensor is not None else None,
                    )

                    if combine:
                        # Combine masks using logical OR
                        combined_mask = np.logical_or.reduce(out_masks_np).astype(np.uint8)
                        mask_tensor_combined = torch.from_numpy(combined_mask).float()
                        out_masks.append(mask_tensor_combined.unsqueeze(0))  # Shape: [1, H, W]
                    else:
                        # Convert each mask to tensor and stack them
                        mask_tensors = [torch.from_numpy(mask).float() for mask in out_masks_np]
                        mask_batch = torch.stack(mask_tensors, dim=0)  # Shape: [num_masks, H, W]
                        out_masks.append(mask_batch)

                if combine:
                    # Concatenate all combined masks into a batch tensor [N, H, W]
                    final_mask = torch.cat(out_masks, dim=0)  # Shape: [N, H, W]
                else:
                    # Stack all mask batches into a single tensor [total_num_masks, H, W]
                    final_mask = torch.cat(out_masks, dim=0)  # Shape: [total_num_masks, H, W]

                # Ensure the mask has the correct shape for downstream nodes
                # If necessary, add a channel dimension
                if len(final_mask.shape) == 3:
                    final_mask = final_mask.unsqueeze(1)  # Shape: [N, 1, H, W]

                return (final_mask,)
            else:
                # Handle other segmentor types if needed
                raise NotImplementedError(f"Segmentor '{segmentor}' is not implemented.")

        if not keep_model_loaded:
            try:
                model.to(offload_device)
            except Exception as e:
                print("Error offloading model:", e)
                model.model.to(offload_device)

        # Fallback return in case of no segmentation
        return (torch.zeros((1, 1, 64, 64), dtype=torch.float32, device="cpu"),)

class CTGPhrases:
    """
    A ComfyUI node class that parses a specially formatted string and outputs a list of phrases.

    The input string should follow the pattern:
    "Phrase<loc_num><loc_num>...Phrase<loc_num>...".

    For each phrase, every 4 <loc_num> entries correspond to one repetition of the phrase in the output list.

    Example:
        Input: "A fountain<loc_424><loc_482><loc_565><loc_721>carved figures of lovers<loc_477>...<loc_804>its water<loc_221><loc_449><loc_730><loc_952>"
        Output: ["A fountain", "carved figures of lovers", "carved figures of lovers", ..., "its water"]
    """

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "input_string": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "parse_string"
    CATEGORY = "GR85/Florence2"

    def parse_string(self, input_string: str) -> Tuple[List[str],]:
        """
        Parses the input string and returns a list of phrases based on the number of <loc_num> entries.

        Args:
            input_string (str): The input string following the specified pattern.

        Returns:
            Tuple[List[str],]: A tuple containing the list of parsed phrases.
        """
        if not input_string:
            print("Input string is empty.")
            return ([],)

        # Regular expression patterns
        phrase_pattern = r'([^<]+)'  # Matches any characters except '<'
        loc_pattern = r'<loc_\d+>'    # Matches <loc_num> patterns

        # Combined pattern to find all phrases and their loc_nums
        combined_pattern = re.compile(rf'{phrase_pattern}((?:{loc_pattern})+)')

        # Find all matches
        matches = combined_pattern.findall(input_string)

        if not matches:
            print("No valid phrases found in the input string.")
            return ([],)

        output_phrases = []

        for phrase, locs in matches:
            # Count the number of <loc_num> entries
            loc_count = len(re.findall(loc_pattern, locs))

            # Determine the number of times to repeat the phrase
            repeat_times = math.ceil(loc_count / 4) if loc_count > 0 else 0

            # Append the phrase the required number of times
            for _ in range(repeat_times):
                output_phrases.append(phrase.strip())

        print(f"Parsed phrases: {output_phrases}")
        return (output_phrases,)


import re
from typing import List, Tuple


class CTGPhrasesSimple:
    """
    A ComfyUI node class that parses a specially formatted string and outputs a list of phrases.

    The input string should follow the pattern:
    "Phrase<loc_num><loc_num>...Phrase<loc_num>...".

    This version removes all <loc_num> tags and returns a list of unique phrases.

    Example:
        Input: "A fountain<loc_424><loc_482>carved figures of lovers<loc_477><loc_804>its water<loc_221>"
        Output: ["A fountain", "carved figures of lovers", "its water"]
    """

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "input_string": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "parse_string"
    CATEGORY = "GR85/Florence2"

    def parse_string(self, input_string: str) -> Tuple[List[str],]:
        """
        Parses the input string and returns a list of phrases with <loc_num> tags removed.

        Args:
            input_string (str): The input string following the specified pattern.

        Returns:
            Tuple[List[str],]: A tuple containing the list of parsed phrases.
        """
        if not input_string:
            print("Input string is empty.")
            return ([],)

        # Regular expression to split the input into phrases and remove <loc_num> tags
        phrase_pattern = r'([^<]+)'  # Matches any characters except '<'
        loc_pattern = r'<loc_\d+>'  # Matches <loc_num> tags

        # Combined pattern to extract phrases and ignore <loc_num> tags
        combined_pattern = re.compile(rf'{phrase_pattern}(?:{loc_pattern})*')

        # Find all phrases
        phrases = combined_pattern.findall(input_string)

        # Clean up and strip whitespace
        output_phrases = [phrase.strip() for phrase in phrases if phrase.strip()]

        print(f"Extracted phrases: {output_phrases}")
        return (output_phrases,)
