import json
import os

class JSONFileReader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {
                    "default": "prompt.json",
                    "display": "file path"
                }),
            }
        }

    RETURN_TYPES = ("INT", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("seed", "positive", "negative", "wildcard")

    FUNCTION = "read_from_json"

    CATEGORY = "GR85/Prompt"

    def read_from_json(self, file_path):
        """
        Reads the JSON file from the comfyui/output directory and returns the seed, positive, negative, and wildcard values.
        """
        try:
            # Determine the root directory and target directory
            root_directory = os.path.abspath(os.curdir)
            target_directory = os.path.join(root_directory, 'comfyui', 'output')

            # Normalize the file path to the correct format for the OS
            normalized_file_path = os.path.normpath(os.path.join(target_directory, file_path))

            # Print the root directory and target directory for reference
            print(f"Root Directory: {root_directory}")
            print(f"Target Directory: {target_directory}")
            print(f"Normalized File Path: {normalized_file_path}")

            # Check if the file exists
            if not os.path.exists(normalized_file_path):
                raise FileNotFoundError(f"The file {normalized_file_path} does not exist.")

            # Read the JSON file
            with open(normalized_file_path, 'r') as json_file:
                data = json.load(json_file)

            # Extract values from the JSON data
            seed = data.get("seed", 0)
            positive = data.get("positive", "")
            negative = data.get("negative", "")
            wildcard = data.get("wildcard", "")

            return seed, positive, negative, wildcard
        except FileNotFoundError as fnf_error:
            print(f"FileNotFoundError: {fnf_error}")
            return 0, "", "", ""
        except PermissionError as perm_error:
            print(f"PermissionError: {perm_error}")
            return 0, "", "", ""
        except json.JSONDecodeError as json_error:
            print(f"JSONDecodeError: {json_error}")
            return 0, "", "", ""
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return 0, "", "", ""
