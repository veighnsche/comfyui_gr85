class SeedBasedOutputSelector:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed_number": ("INT", {"forceInput": True, "default": 0}),
            },
            "optional": {
                "input_1": ("STRING", {"forceInput": True, "default": None}),
                "input_2": ("STRING", {"forceInput": True, "default": None}),
                "input_3": ("STRING", {"forceInput": True, "default": None}),
                "input_4": ("STRING", {"forceInput": True, "default": None}),
                "input_5": ("STRING", {"forceInput": True, "default": None}),
                "input_6": ("STRING", {"forceInput": True, "default": None}),
                "input_7": ("STRING", {"forceInput": True, "default": None}),
                "input_8": ("STRING", {"forceInput": True, "default": None}),
                "input_9": ("STRING", {"forceInput": True, "default": None}),
                "input_10": ("STRING", {"forceInput": True, "default": None}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_output",)

    FUNCTION = "select_output"

    CATEGORY = "GR85/Prompt"

    def select_output(self, seed_number, input_1=None, input_2=None, input_3=None, input_4=None, input_5=None, input_6=None, input_7=None, input_8=None, input_9=None, input_10=None):
        """
        Select an output based on the seed number and available non-null inputs.
        """

        # Collect all inputs into a list
        inputs = [input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10]

        # Filter out the null inputs (None)
        non_null_inputs = [i for i in inputs if i is not None]

        # Count the number of non-null inputs
        num_outputs = len(non_null_inputs)

        # If no non-null inputs exist, return an empty string or some indication of no valid input
        if num_outputs == 0:
            return ("",)

        # Perform modulus operation with the number of non-null inputs
        output_index = seed_number % num_outputs

        # Select the correct output from the list of non-null inputs
        final_output = non_null_inputs[output_index]

        return (final_output,)
