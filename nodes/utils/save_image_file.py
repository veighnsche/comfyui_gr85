import os
import re
from PIL import Image
import numpy as np
import torch

class SaveImageFile:
    """
    A ComfyUI node class that saves an image to a file based on given inputs.

    Attributes:
        INPUT_TYPES (dict): Defines the required and optional input types for the node.
        RETURN_TYPES (tuple): Specifies the types of values returned by the node.
        RETURN_NAMES (tuple): Specifies the names of the returned values for better identification.
        FUNCTION (str): The function name used for processing parameters.
        CATEGORY (str): The category under which this node is classified.
    """

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "image": ("IMAGE", ),  # The image to be saved.
                "path": ("STRING", {"default": './ComfyUI/output/'}),  # Directory path where the file will be saved.
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),  # Prefix for the filename.
                "filename_delimiter": ("STRING", {"default": "_"}),  # Delimiter between prefix and number.
                "filename_number_padding": ("INT", {"default": 4, "min": 0, "max": 9, "step": 1}),  # Number of padding zeros for the filename.
            },
            "optional": {
                "file_extension": ("STRING", {"default": ".png"}),  # File extension for the saved file.
            }
        }

    OUTPUT_NODE = True
    RETURN_TYPES = ()
    FUNCTION = "save_image_file"
    CATEGORY = "GR85/Utils"

    def save_image_file(self, image, path: str, filename_prefix: str = 'ComfyUI', filename_delimiter: str = '_', filename_number_padding: int = 4, file_extension: str = '.png'):
        # Ensure the directory exists, create if it does not exist
        if not os.path.exists(path):
            print(f"The path `{path}` doesn't exist! Creating it...")
            try:
                os.makedirs(path, exist_ok=True)
            except OSError as e:
                # If directory creation fails, print an error and return
                print(f"The path `{path}` could not be created! Is there write access?\n{e}")
                return (image,)

        # If the image is None, print an error and return
        if image is None:
            print(f"No image specified to save! Image is None.")
            return (image,)

        delimiter = filename_delimiter
        number_padding = int(filename_number_padding)
        # Generate the filename using the specified parameters
        filename = self.generate_filename(path, filename_prefix, delimiter, number_padding, file_extension)
        file_path = os.path.join(path, filename)
        # Write the image to the file
        self.write_image_file(file_path, image)
        return (image,)

    def generate_filename(self, path: str, prefix: str, delimiter: str, number_padding: int, extension: str) -> str:
        # Generate a filename based on the given parameters
        if number_padding == 0:
            # If number_padding is 0, don't use a numerical suffix
            filename = f"{prefix}{extension}"
        else:
            # Create a regex pattern to match existing files with the specified prefix and delimiter
            pattern = f"{re.escape(prefix)}{re.escape(delimiter)}(\\d{{{number_padding}}}){re.escape(extension)}"
            # Find all existing files that match the pattern and extract their counters
            existing_counters = [
                int(re.search(pattern, filename).group(1))
                for filename in os.listdir(path)
                if re.match(pattern, filename)
            ]
            # Sort counters in descending order to find the highest value
            existing_counters.sort(reverse=True)
            if existing_counters:
                # Set the next counter value to the highest existing value plus one
                counter = existing_counters[0] + 1
            else:
                # If no existing files, start with counter 1
                counter = 1
            # Format the filename with the prefix, delimiter, counter, and extension
            filename = f"{prefix}{delimiter}{counter:0{number_padding}}{extension}"
            # Ensure the generated filename does not already exist
            while os.path.exists(os.path.join(path, filename)):
                counter += 1
                filename = f"{prefix}{delimiter}{counter:0{number_padding}}{extension}"
        return filename

    def write_image_file(self, file_path: str, image):
        try:
            print(f"Type of image input: {type(image)}")
            if isinstance(image, dict) and 'samples' in image:
                image_tensor = image['samples']
                print(f"Image tensor shape: {image_tensor.shape}")
                image_to_save = self.tensor_to_image(image_tensor)
            elif isinstance(image, torch.Tensor):
                print(f"Image tensor shape: {image.shape}")
                image_to_save = self.tensor_to_image(image)
            elif isinstance(image, Image.Image):
                print("Image is a PIL Image.")
                image_to_save = image
            elif isinstance(image, np.ndarray):
                print("Image is a NumPy array.")
                image_to_save = Image.fromarray(image)
            else:
                print(f"Unsupported image type: {type(image)}")
                return
            if image_to_save is None:
                print("Error converting image to a saveable format.")
                return
            image_to_save.save(file_path)
            print(f"Image saved successfully at {file_path}")
        except Exception as e:
            print(f"Unable to save image file `{file_path}`: {e}")

    def tensor_to_image(self, tensor):
        try:
            print(f"Original tensor shape: {tensor.shape}")
            # Remove batch dimension if present
            if tensor.dim() == 4 and tensor.size(0) == 1:
                tensor = tensor.squeeze(0)
                print(f"Tensor after squeezing batch dimension: {tensor.shape}")
            # Now tensor should be [height, width, channels]
            if tensor.dim() == 3:
                image_np = tensor.detach().cpu().numpy()
                # Handle pixel value scaling
                if image_np.max() <= 1.0:
                    image_np = (image_np * 255).clip(0, 255).astype(np.uint8)
                else:
                    image_np = image_np.clip(0, 255).astype(np.uint8)
                image = Image.fromarray(image_np)
                return image
            else:
                print(f"Unsupported tensor shape: {tensor.shape}")
                return None
        except Exception as e:
            print(f"Error converting tensor to image: {e}")
            return None
