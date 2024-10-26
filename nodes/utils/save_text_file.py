import os
import re

class SaveTextFile:
    """
    A ComfyUI node class that saves text to a file based on given inputs.

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
                "text": ("STRING", {"forceInput": True, "multiline": True}),  # The text content to be saved.
                "path": ("STRING", {"default": './ComfyUI/output/', "multiline": True}),  # Directory path where the file will be saved.
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),  # Prefix for the filename.
                "filename_delimiter": ("STRING", {"default": "_"}),  # Delimiter between prefix and number.
                "filename_number_padding": ("INT", {"default": 4, "min": 0, "max": 9, "step": 1}),  # Number of padding zeros for the filename.
            },
            "optional": {
                "file_extension": ("STRING", {"default": ".txt"}),  # File extension for the saved file.
                "encoding": ("STRING", {"default": "utf-8"})  # Encoding to use when writing the file.
            }
        }

    OUTPUT_NODE = True
    RETURN_TYPES = ()
    FUNCTION = "save_text_file"
    CATEGORY = "GR85/Utils"

    def save_text_file(self, text: str, path: str, filename_prefix: str = 'ComfyUI', filename_delimiter: str = '_', filename_number_padding: int = 4, file_extension: str = '.txt', encoding: str = 'utf-8'):
        # Ensure the directory exists, create if it does not exist
        if not os.path.exists(path):
            print(f"The path `{path}` doesn't exist! Creating it...")
            try:
                os.makedirs(path, exist_ok=True)
            except OSError as e:
                # If directory creation fails, print an error and return
                print(f"The path `{path}` could not be created! Is there write access?\n{e}")
                return

        # If the text is empty, print an error and return
        if text.strip() == '':
            print(f"There is no text specified to save! Text is empty.")
            return

        delimiter = filename_delimiter
        number_padding = int(filename_number_padding)
        # Generate the filename using the specified parameters
        filename = self.generate_filename(path, filename_prefix, delimiter, number_padding, file_extension)
        file_path = os.path.join(path, filename)
        # Write the text content to the file
        self.write_text_file(file_path, text, encoding)
        return (text, {"ui": {"string": text}})

    def generate_filename(self, path: str, prefix: str, delimiter: str, number_padding: int, extension: str) -> str:
        # Generate a filename based on the given parameters
        if number_padding == 0:
            # If number_padding is 0, don't use a numerical suffix
            filename = f"{prefix}{extension}"
        else:
            # Create a regex pattern to match existing files with the specified prefix and delimiter
            pattern = f"{re.escape(prefix)}{re.escape(delimiter)}(\d{{{number_padding}}})"
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

    def write_text_file(self, file: str, content: str, encoding: str):
        # Write the content to the specified file with the given encoding
        try:
            with open(file, 'w', encoding=encoding, newline='\n') as f:
                f.write(content)
        except OSError:
            # Print an error message if the file could not be saved
            print(f"Unable to save file `{file}`")

# Let me know if you need to customize or extend this node further!
