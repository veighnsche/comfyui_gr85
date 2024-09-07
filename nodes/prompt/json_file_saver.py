import json
import os

class JSONFileSaver:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {
                    "forceInput": True,
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "display": "number"
                }),
                "positive": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "display": "text"
                }),
                "negative": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "display": "text"
                }),
                "wildcard": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "display": "text"
                }),
                "file_path": ("STRING", {
                    "default": "prompt.json",
                    "display": "file path"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_string",)

    FUNCTION = "save_to_json"

    CATEGORY = "GR85/Prompt"

    def save_to_json(self, seed, positive, negative, wildcard, file_path):
        """
        Saves the given inputs to a .json file in the ComfyUI/output directory
        and returns the stringified version of the JSON data.
        """
        data = {
            "seed": seed,
            "positive": positive,
            "negative": negative,
            "wildcard": wildcard
        }

        try:
            # Determine the root directory and target directory
            root_directory = os.path.abspath(os.curdir)
            target_directory = os.path.join(root_directory, 'ComfyUI', 'output')

            # Normalize the file path to the correct format for the OS
            normalized_file_path = os.path.normpath(os.path.join(target_directory, file_path))

            # Print the root directory and target directory for reference
            print(f"Root Directory: {root_directory}")
            print(f"Target Directory: {target_directory}")
            print(f"Normalized File Path: {normalized_file_path}")

            # Extract the directory from the normalized file path
            directory = os.path.dirname(normalized_file_path)

            # Create the target directory if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Directory {directory} created.")

            # Convert the dictionary to a JSON string
            json_string = json.dumps(data, indent=4)

            # Save the JSON string to the file
            with open(normalized_file_path, 'w') as json_file:
                json_file.write(json_string)

            print(f"Data successfully saved to {normalized_file_path}")
            return (json_string,)
        except FileNotFoundError as fnf_error:
            print(f"FileNotFoundError: {fnf_error}")
            return ("Error: File or directory not found",)
        except PermissionError as perm_error:
            print(f"PermissionError: {perm_error}")
            return ("Error: Permission denied",)
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")
            return (f"Error: {str(e)}",)
