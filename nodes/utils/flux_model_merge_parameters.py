import random
from typing import Optional

class FluxModelMergeParameters:
    """
    A utility class for generating and handling parameters for model merging operations.

    This class supports two modes of operation:
    - **User-Provided Values**: Accepts a comma-separated string of values provided by the user.
    - **Random Value Generation**: Generates random values using a specified seed, with optional bias adjustments.

    Attributes:
        INPUT_TYPES (dict): Defines the required and optional input types for the node.
        RETURN_TYPES (tuple): Specifies the types of values returned by the node.
        RETURN_NAMES (tuple): Specifies the names of the returned values for better identification.
        FUNCTION (str): The function name used for processing parameters.
        CATEGORY (str): The category under which this node is classified.

    Key Concepts:
        - **Bias Adjustment**: Adjusts the generated random values to achieve a target average (`bias`), while maintaining randomness.
        - **Parameter Distribution**: Supports generating parameters that are evenly distributed or skewed towards a specific average value.

    Notes:
        - The goal is to prioritize randomness over precision. The bias adjustment aims to influence the average value of the parameters
          without significantly reducing randomness.
    """

    def __init__(self):
        pass  # No initialization required for this utility class.

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        """
        Defines the required and optional input types for the node.

        Returns:
            dict: A dictionary containing the input parameters with their types and constraints.
        """
        return {
            "required": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,  # Maximum 64-bit unsigned integer
                    "step": 1,
                    "display": "number"
                }),
                "bias": ("FLOAT", {
                    "default": 0.5,  # Neutral bias
                    "min": 0.00,
                    "max": 1.00,
                    "step": 0.01,
                }),
                "use_bias": ("BOOLEAN", {"default": False}),
                "max_percentage_change": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.01,
                    "max": 0.5,
                    "step": 0.01,
                }),
            },
            "optional": {
                "values": ("STRING", {
                    "default": "",
                    "multiline": True  # Allows multi-line input
                })
            }
        }

    # Constants for readability and maintainability
    # Define the structure of the parameters
    IMAGE_INPUTS = ("FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT")
    DOUBLE_BLOCKS = tuple("FLOAT" for _ in range(19))
    SINGLE_BLOCKS = tuple("FLOAT" for _ in range(38))
    FINAL_LAYER = ("FLOAT",)
    TOTAL_PARAMETERS = 5 + 19 + 38 + 1  # Sum of all parameters

    # Defines the types of values returned by the node
    RETURN_TYPES = (
        "STRING",  # Comma-separated values
        *IMAGE_INPUTS,
        *DOUBLE_BLOCKS,
        *SINGLE_BLOCKS,
        *FINAL_LAYER
    )

    # Names corresponding to each parameter
    IMAGE_INPUT_NAMES = ("img_in", "time_in", "guidance_in", "vector_in", "txt_in")
    DOUBLE_BLOCK_NAMES = tuple(f"double_blocks_{i}" for i in range(19))
    SINGLE_BLOCK_NAMES = tuple(f"single_blocks_{i}" for i in range(38))
    FINAL_LAYER_NAME = ("final_layer",)

    # Combines all return names into a single tuple
    RETURN_NAMES = (
        "comma_separated_values",
        *IMAGE_INPUT_NAMES,
        *DOUBLE_BLOCK_NAMES,
        *SINGLE_BLOCK_NAMES,
        *FINAL_LAYER_NAME
    )

    FUNCTION = "process_parameters"
    CATEGORY = "GR85/Utils"

    def process_parameters(
            self,
            seed: int,
            bias: float,
            use_bias: bool,
            max_percentage_change: float,
            values: Optional[str] = None,
    ):
        """
        Generates parameter values either based on user input or using a random seed.

        Args:
            seed (int): Seed for the random number generator to ensure reproducibility.
            bias (float): The target average value for the generated parameters (0.0 to 1.0).
            use_bias (bool): If True, adjusts the generated values to achieve the specified bias.
            max_percentage_change (float): Maximum deviation allowed when adjusting values to meet the bias.
            values (Optional[str]): Comma-separated string of values provided by the user. If None, random values are generated.

        Returns:
            tuple: A tuple containing the comma-separated values and all the individual float values.

        Raises:
            ValueError: If the provided values are not numeric or do not match the expected number of parameters.

        Notes:
            - The method aims to adjust the average value of the parameters towards the desired bias without significantly
              affecting the randomness.
            - The adjustment is done by modifying the range from which random values are drawn for the second half of the parameters.
            - Randomness is prioritized over achieving an exact bias.
        """
        if values:
            # User has provided a string of values
            try:
                # Parse the string into a list of floats
                value_list = [float(v.strip()) for v in values.split(",") if v.strip()]
            except ValueError as e:
                # Raise an error if parsing fails
                raise ValueError("All provided values must be numeric.") from e

            # Check if the number of values matches the expected total
            if len(value_list) != self.TOTAL_PARAMETERS:
                raise ValueError(
                    f"The provided values must match the expected number of parameters ({self.TOTAL_PARAMETERS})."
                )
            # Proceed with the provided values
        else:
            # No values provided; generate random values
            random.seed(seed)  # Seed the random number generator for reproducibility
            total_params = self.TOTAL_PARAMETERS

            # Initialize the list to hold parameter values
            value_list = []

            if not use_bias:
                # If bias adjustment is not requested, generate random values uniformly in [0.0, 1.0]
                value_list = [random.uniform(0.0, 1.0) for _ in range(total_params)]
            else:
                # Bias adjustment is requested
                # Generate random values for the first half without adjustment
                half_index = total_params // 2
                for _ in range(half_index):
                    value_list.append(random.uniform(0.0, 1.0))

                # For the second half, adjust the range of random values to steer the average towards the desired bias
                for _ in range(half_index, total_params):
                    # Calculate the current average
                    current_average = sum(value_list) / len(value_list)

                    # Determine the adjustment direction based on current average and desired bias
                    if current_average < bias:
                        # If current average is less than desired bias, generate higher values
                        # Increase min_val to pull average up
                        adjustment = max_percentage_change * (1.0 - current_average)
                        min_val = min(1.0, current_average + adjustment)
                        max_val = 1.0  # Max value remains at 1.0
                    else:
                        # If current average is greater than desired bias, generate lower values
                        # Decrease max_val to pull average down
                        adjustment = max_percentage_change * current_average
                        min_val = 0.0  # Min value remains at 0.0
                        max_val = max(0.0, current_average - adjustment)

                    # Ensure min_val is not greater than max_val
                    if min_val > max_val:
                        min_val, max_val = max_val, min_val

                    # Generate the next random value within the adjusted range
                    next_value = random.uniform(min_val, max_val)
                    value_list.append(next_value)

                    # Debugging information (can be commented out or removed in production)
                    # print(f"Generated value: {next_value}, min_val: {min_val}, max_val: {max_val}")

                # If total_params is odd, we need to generate one more value
                if total_params % 2 != 0:
                    current_average = sum(value_list) / len(value_list)
                    if current_average < bias:
                        min_val = current_average
                        max_val = 1.0
                    else:
                        min_val = 0.0
                        max_val = current_average
                    next_value = random.uniform(min_val, max_val)
                    value_list.append(next_value)

            # Shuffle the values to maintain randomness and avoid any patterns
            random.shuffle(value_list)

        # Create a comma-separated string of all values for reference
        comma_separated_values = ", ".join(map(str, value_list))

        # Return the comma-separated string and unpack the list of values
        return (comma_separated_values, *value_list)
