class IntegerSequenceModifier:
    """
    A ComfyUI node class that generates a sequence of integers, modifies the sequence based on an index value,
    and returns a comma-separated string representation of the sequence.

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
                "starting_int": ("INT", {
                    "default": 0,
                    "min": 0,
                    "step": 1,
                    "display": "number"
                }),
                "amount_of_ints": ("INT", {
                    "default": 5,
                    "min": 1,
                    "step": 1,
                    "display": "number"
                }),
                "index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "step": 1,
                    "display": "number"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("comma_separated_list",)

    FUNCTION = "modify_sequence"
    CATEGORY = "GR85/Utils"

    def modify_sequence(self, starting_int: int, amount_of_ints: int, index: int) -> tuple:
        """
        Generates a sequence of integers starting from a given value, modifies the sequence based on the index,
        and returns the modified sequence as a comma-separated string.

        Args:
            starting_int (int): The starting integer of the sequence.
            amount_of_ints (int): The number of integers to generate in the sequence.
            index (int): The index value used to modify the sequence.

        Returns:
            tuple: A tuple containing a comma-separated list of integers in string form.
        """
        # Generate the list of integers
        int_list = [starting_int + i for i in range(amount_of_ints)]

        # Apply the index logic to adjust the values
        for i in range(index):
            int_list[i % amount_of_ints] += amount_of_ints

        # Convert the list to a comma-separated string
        comma_separated_list = ", ".join(map(str, int_list))

        return (comma_separated_list,)
