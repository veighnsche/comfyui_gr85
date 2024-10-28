import random
import logging
from typing import Optional, List, Tuple, Dict

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
    """

    # Constants for parameter groups
    IMAGE_INPUTS = ("FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT")
    DOUBLE_BLOCKS = tuple("FLOAT" for _ in range(19))
    SINGLE_BLOCKS = tuple("FLOAT" for _ in range(38))
    FINAL_LAYER = ("FLOAT",)
    PARAMETER_GROUPS = {
        "image_inputs": 5,
        "double_blocks": 19,
        "single_blocks": 38,
        "final_layer": 1
    }
    TOTAL_PARAMETERS = sum(PARAMETER_GROUPS.values())  # 63

    # Return types and names
    RETURN_TYPES = (
        "STRING",  # Comma-separated values
        "FLOAT",
        *IMAGE_INPUTS,
        *DOUBLE_BLOCKS,
        *SINGLE_BLOCKS,
        *FINAL_LAYER
    )

    IMAGE_INPUT_NAMES = ("img_in", "time_in", "guidance_in", "vector_in", "txt_in")
    DOUBLE_BLOCK_NAMES = tuple(f"double_blocks_{i}" for i in range(19))
    SINGLE_BLOCK_NAMES = tuple(f"single_blocks_{i}" for i in range(38))
    FINAL_LAYER_NAME = ("final_layer",)

    RETURN_NAMES = (
        "comma_separated_values",
        "average_value",
        *IMAGE_INPUT_NAMES,
        *DOUBLE_BLOCK_NAMES,
        *SINGLE_BLOCK_NAMES,
        *FINAL_LAYER_NAME
    )

    FUNCTION = "process_parameters"
    CATEGORY = "GR85/Utils"

    def __init__(self):
        # Initialize the logger
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.WARNING)  # Default level

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Dict]]:
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
                "only_blocks": ("BOOLEAN", {"default": False}),
                "default_float": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "only_0_and_1": ("BOOLEAN", {"default": False}),
                "enable_shuffle": ("BOOLEAN", {"default": True}),  # Option to enable/disable shuffling
                "debug": ("BOOLEAN", {"default": False})  # New debug input
            },
            "optional": {
                "values": ("STRING", {
                    "default": "",
                    "multiline": True  # Allows multi-line input
                })
            }
        }

    def process_parameters(
            self,
            seed: int,
            bias: float,
            use_bias: bool,
            max_percentage_change: float,
            only_blocks: bool,
            default_float: float,
            only_0_and_1: bool,
            enable_shuffle: bool,
            debug: bool,  # New debug parameter
            values: Optional[str] = None,
    ) -> Tuple:
        """
        Generates parameter values either based on user input or using a random seed.

        Args:
            seed (int): Seed for the random number generator to ensure reproducibility.
            bias (float): The target average value for the generated parameters (0.0 to 1.0).
            use_bias (bool): If True, adjusts the generated values to achieve the specified bias.
            max_percentage_change (float): Maximum deviation allowed when adjusting values to meet the bias.
            only_blocks (bool): If True, only the blocks get random floats, others get the default_float value.
            default_float (float): Value assigned to non-block parameters if only_blocks is True.
            only_0_and_1 (bool): If True, generates only 0 or 1 for the parameter values.
            enable_shuffle (bool): If True, shuffles the final list of values to maintain randomness.
            debug (bool): If True, enables debug logging.
            values (Optional[str]): Comma-separated string of values provided by the user. If None, random values are generated.

        Returns:
            tuple: A tuple containing the comma-separated values and all the individual float values.

        Raises:
            ValueError: If the provided values are not numeric or do not match the expected number of parameters.

        Notes:
            - The method aims to adjust the average value of the parameters towards the desired bias without significantly
              affecting the randomness.
            - The adjustment is done across all relevant parameters to ensure uniform influence.
            - Shuffling is performed within parameter groups to maintain structural integrity if needed.
        """
        # Configure logging based on the debug flag
        if debug:
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug("Debugging is enabled.")
        else:
            self.logger.setLevel(logging.WARNING)

        self.logger.debug(f"Starting process_parameters with seed={seed}, bias={bias}, use_bias={use_bias}, "
                          f"max_percentage_change={max_percentage_change}, only_blocks={only_blocks}, "
                          f"default_float={default_float}, only_0_and_1={only_0_and_1}, "
                          f"enable_shuffle={enable_shuffle}, values={'Provided' if values else 'None'}.")

        if values:
            # User has provided a string of values
            self.logger.debug("Parsing user-provided values.")
            value_list = self._parse_user_values(values)
            if only_blocks:
                self.logger.debug("only_blocks=True: Overriding non-block parameters with default_float.")
                # Override non-block parameters with default_float
                for i, name in enumerate(self.IMAGE_INPUT_NAMES):
                    index = self.RETURN_NAMES.index(name) - 2  # Adjust for comma_separated_values and average_value
                    original_value = value_list[index]
                    value_list[index] = default_float
                    self.logger.debug(f"Set {name} from {original_value} to default_float={default_float}.")
        else:
            # No values provided; generate random values
            self.logger.debug("Generating random values.")
            random.seed(seed)  # Seed the random number generator for reproducibility
            value_list = self._generate_random_values(
                use_bias=use_bias,
                bias=bias,
                max_percentage_change=max_percentage_change,
                only_blocks=only_blocks,
                default_float=default_float,
                only_0_and_1=only_0_and_1,
                enable_shuffle=enable_shuffle
            )

        comma_separated_values = ", ".join(map(str, value_list))
        average_value = sum(value_list) / len(value_list)

        self.logger.debug(f"Generated comma-separated values: {comma_separated_values}")
        self.logger.debug(f"Average value of parameters: {average_value}")

        # Create a mapping from names to values for clarity (optional, can be used for debugging)
        named_values = {
            name: value for name, value in zip(self.RETURN_NAMES[2:], value_list)  # Skip comma_separated_values and average_value
        }

        self.logger.debug(f"Named values: {named_values}")

        # Ensure non-block parameters are set to default_float when only_blocks is True
        if only_blocks:
            for name in self.IMAGE_INPUT_NAMES:
                index = self.RETURN_NAMES.index(name) - 2
                assert value_list[index] == default_float, f"{name} is not set to default_float={default_float}."
                self.logger.debug(f"Assertion passed: {name} is correctly set to default_float={default_float}.")

        # Order the return values as per RETURN_NAMES
        ordered_values = (
            comma_separated_values,
            average_value,
            *value_list,  # Include all parameter values
        )

        self.logger.debug("process_parameters completed successfully.")
        self.logger.debug(f"Ordered return values: {ordered_values}")

        return ordered_values

    def _parse_user_values(self, values: str) -> List[float]:
        """
        Parses and validates user-provided comma-separated values.

        Args:
            values (str): Comma-separated string of values.

        Returns:
            List[float]: List of parsed float values.

        Raises:
            ValueError: If parsing fails or the number of values is incorrect.
        """
        self.logger.debug("Entering _parse_user_values.")
        try:
            # Parse the string into a list of floats
            value_list = [float(v.strip()) for v in values.split(",") if v.strip()]
            self.logger.debug(f"Parsed values: {value_list}")
        except ValueError as e:
            # Raise an error if parsing fails
            self.logger.error("Failed to parse user-provided values. All values must be numeric.")
            raise ValueError("All provided values must be numeric.") from e

        # Check if the number of values matches the expected total
        if len(value_list) != self.TOTAL_PARAMETERS:
            self.logger.error(f"Incorrect number of values provided. Expected {self.TOTAL_PARAMETERS}, got {len(value_list)}.")
            raise ValueError(
                f"The provided values must match the expected number of parameters ({self.TOTAL_PARAMETERS}). "
                f"Please ensure you provide exactly {self.TOTAL_PARAMETERS} comma-separated values."
            )

        self.logger.debug("User-provided values parsed and validated successfully.")
        return value_list

    def _generate_random_values(
            self,
            use_bias: bool,
            bias: float,
            max_percentage_change: float,
            only_blocks: bool,
            default_float: float,
            only_0_and_1: bool,
            enable_shuffle: bool
    ) -> List[float]:
        """
        Generates random parameter values based on the provided configurations.

        Args:
            use_bias (bool): Whether to apply bias adjustment.
            bias (float): Target average value.
            max_percentage_change (float): Maximum allowed adjustment per parameter.
            only_blocks (bool): Whether to only randomize block parameters.
            default_float (float): Default value for non-block parameters if only_blocks is True.
            only_0_and_1 (bool): Whether to restrict values to 0 and 1.
            enable_shuffle (bool): Whether to shuffle the parameters.

        Returns:
            List[float]: Generated list of parameter values.
        """
        self.logger.debug("Entering _generate_random_values.")
        value_list = []

        if only_blocks:
            # Initialize the entire list with default_float
            self.logger.debug(f"only_blocks=True: Initializing all {self.TOTAL_PARAMETERS} parameters to default_float={default_float}.")
            value_list = [default_float] * self.TOTAL_PARAMETERS
        else:
            # Initialize all parameters to 0.0
            self.logger.debug("only_blocks=False: Initializing all parameters to 0.0 before generation.")
            value_list = [0.0] * self.TOTAL_PARAMETERS

        # Identify block indices
        block_start = self.PARAMETER_GROUPS["image_inputs"]
        block_end = (
                self.PARAMETER_GROUPS["image_inputs"] +
                self.PARAMETER_GROUPS["double_blocks"] +
                self.PARAMETER_GROUPS["single_blocks"] +
                self.PARAMETER_GROUPS["final_layer"]
        )
        block_indices = list(range(block_start, block_end))
        self.logger.debug(f"Block indices: {block_indices}")

        if only_blocks:
            self.logger.debug("Generating values for block parameters with only_blocks=True.")
            block_values = self._generate_block_values(
                use_bias=use_bias,
                bias=bias,
                max_percentage_change=max_percentage_change,
                only_0_and_1=only_0_and_1,
                enable_shuffle=enable_shuffle
            )
            self.logger.debug(f"Generated block values: {block_values}")
            # Ensure that the number of block_values matches the number of block_indices
            if len(block_values) != len(block_indices):
                self.logger.error(f"Mismatch in block values count. Expected {len(block_indices)}, got {len(block_values)}.")
                raise ValueError("Number of block values does not match number of block indices.")

            for idx, val in zip(block_indices, block_values):
                value_list[idx] = val
                self.logger.debug(f"Set parameter at index {idx} to {val}.")
        else:
            # Handle other scenarios where only_blocks=False
            self.logger.debug("Generating values for all parameters with only_blocks=False.")
            if only_0_and_1:
                if use_bias:
                    self.logger.debug("only_0_and_1=True and use_bias=True: Generating binary values with bias.")
                    block_values = self._generate_binary_values_with_bias(
                        count=self.TOTAL_PARAMETERS,
                        bias=bias,
                        enable_shuffle=enable_shuffle
                    )
                else:
                    self.logger.debug("only_0_and_1=True and use_bias=False: Generating random binary values.")
                    block_values = [random.choice([0.0, 1.0]) for _ in range(self.TOTAL_PARAMETERS)]
            else:
                if use_bias:
                    self.logger.debug("only_0_and_1=False and use_bias=True: Generating float values with bias.")
                    block_values = self._generate_floats_with_bias(
                        count=self.TOTAL_PARAMETERS,
                        bias=bias,
                        max_percentage_change=max_percentage_change
                    )
                else:
                    self.logger.debug("only_0_and_1=False and use_bias=False: Generating uniformly random float values.")
                    block_values = [random.uniform(0.0, 1.0) for _ in range(self.TOTAL_PARAMETERS)]

            self.logger.debug(f"Generated block_values: {block_values}")
            for idx, val in enumerate(block_values):
                value_list[idx] = val
                self.logger.debug(f"Set parameter at index {idx} to {val}.")

        # Shuffle within parameter groups if enabled
        if enable_shuffle:
            self.logger.debug("enable_shuffle=True: Shuffling parameters within their respective groups.")
            value_list = self._shuffle_within_groups(value_list, only_blocks)
        else:
            self.logger.debug("enable_shuffle=False: Skipping shuffling of parameters.")

        self.logger.debug("Exiting _generate_random_values.")
        return value_list

    def _generate_block_values(
            self,
            use_bias: bool,
            bias: float,
            max_percentage_change: float,
            only_0_and_1: bool,
            enable_shuffle: bool  # Added enable_shuffle as a parameter
    ) -> List[float]:
        """
        Generates values for block parameters with optional bias adjustment.

        Args:
            use_bias (bool): Whether to apply bias.
            bias (float): Target average.
            max_percentage_change (float): Maximum adjustment per parameter.
            only_0_and_1 (bool): Whether to restrict to binary values.
            enable_shuffle (bool): Whether to shuffle the binary values after generation.

        Returns:
            List[float]: Generated block values.
        """
        self.logger.debug("Entering _generate_block_values.")
        block_count = self.PARAMETER_GROUPS["double_blocks"] + \
                      self.PARAMETER_GROUPS["single_blocks"] + \
                      self.PARAMETER_GROUPS["final_layer"]
        self.logger.debug(f"Total block parameters to generate: {block_count}")

        if only_0_and_1:
            self.logger.debug("only_0_and_1=True: Generating binary block values.")
            if use_bias:
                self.logger.debug(f"use_bias=True: Generating binary values with bias={bias}.")
                block_values = self._generate_binary_values_with_bias(
                    count=block_count,
                    bias=bias,
                    enable_shuffle=enable_shuffle  # Pass enable_shuffle here
                )
            else:
                self.logger.debug("use_bias=False: Generating random binary values.")
                block_values = [random.choice([0.0, 1.0]) for _ in range(block_count)]
        else:
            if not use_bias:
                self.logger.debug("only_0_and_1=False and use_bias=False: Generating uniformly random float values.")
                block_values = [random.uniform(0.0, 1.0) for _ in range(block_count)]
            else:
                self.logger.debug("only_0_and_1=False and use_bias=True: Generating float values with bias.")
                block_values = self._generate_floats_with_bias(
                    count=block_count,
                    bias=bias,
                    max_percentage_change=max_percentage_change
                )

        self.logger.debug(f"Generated block_values: {block_values}")
        self.logger.debug("Exiting _generate_block_values.")
        return block_values


    def _generate_floats_with_bias(
            self,
            count: int,
            bias: float,
            max_percentage_change: float
    ) -> List[float]:
        """
        Generates float values with bias adjustment.

        Args:
            count (int): Number of values to generate.
            bias (float): Target average.
            max_percentage_change (float): Maximum allowed adjustment per parameter.

        Returns:
            List[float]: Generated float values.
        """
        self.logger.debug(f"Entering _generate_floats_with_bias with count={count}, bias={bias}, "
                          f"max_percentage_change={max_percentage_change}.")
        # Handle edge cases
        if bias <= 0.0:
            self.logger.debug("bias <= 0.0: Returning all zeros.")
            return [0.0] * count
        elif bias >= 1.0:
            self.logger.debug("bias >= 1.0: Returning all ones.")
            return [1.0] * count

        values = []
        total_desired = bias * count
        current_total = 0.0

        for i in range(count):
            remaining = count - i
            desired_remaining = total_desired - current_total
            # Calculate the ideal value for this parameter
            ideal = desired_remaining / remaining
            # Apply max_percentage_change
            adjustment = max_percentage_change * ideal
            min_val = max(0.0, ideal - adjustment)
            max_val = min(1.0, ideal + adjustment)
            self.logger.debug(f"Parameter {i}: ideal={ideal}, adjustment={adjustment}, min_val={min_val}, max_val={max_val}")

            next_value = random.uniform(min_val, max_val)
            self.logger.debug(f"Parameter {i}: Generated value={next_value}")
            values.append(next_value)
            current_total += next_value

        # Adjust to ensure the total matches exactly
        current_average = current_total / count
        self.logger.debug(f"Generated float values before adjustment: {values}")
        self.logger.debug(f"Current average: {current_average}, desired bias: {bias}")

        # Optional: Implement a normalization step if precise bias is required
        # For simplicity, this step is omitted

        self.logger.debug("Exiting _generate_floats_with_bias.")
        return values

    def _generate_binary_values_with_bias(
            self,
            count: int,
            bias: float,
            enable_shuffle: bool  # Added enable_shuffle as a parameter
    ) -> List[float]:
        """
        Generates binary (0 or 1) values with a specified bias.

        Args:
            count (int): Number of values to generate.
            bias (float): Target average (proportion of 1s).
            enable_shuffle (bool): Whether to shuffle the binary values after generation.

        Returns:
            List[float]: Generated binary values.
        """
        self.logger.debug(f"Entering _generate_binary_values_with_bias with count={count}, bias={bias}, enable_shuffle={enable_shuffle}.")

        # Handle edge cases
        if bias <= 0.0:
            self.logger.debug("bias <= 0.0: Returning all zeros.")
            return [0.0] * count
        elif bias >= 1.0:
            self.logger.debug("bias >= 1.0: Returning all ones.")
            return [1.0] * count

        num_ones = int(round(count * bias))
        num_zeros = count - num_ones
        self.logger.debug(f"Calculating number of 1s: {num_ones}, number of 0s: {num_zeros}.")

        binary_values = [1.0] * num_ones + [0.0] * num_zeros
        self.logger.debug(f"Generated binary_values before shuffling: {binary_values}")

        if enable_shuffle:
            random.shuffle(binary_values)
            self.logger.debug(f"Shuffled binary_values: {binary_values}")
        else:
            self.logger.debug("Shuffling is disabled: Binary values are not shuffled.")

        self.logger.debug("Exiting _generate_binary_values_with_bias.")
        return binary_values


    def _shuffle_within_groups(
            self,
            value_list: List[float],
            only_blocks: bool
    ) -> List[float]:
        """
        Shuffles the parameter values within their respective groups to maintain structural integrity.

        Args:
            value_list (List[float]): The list of parameter values.
            only_blocks (bool): Whether only block parameters should be shuffled.

        Returns:
            List[float]: Shuffled parameter values.
        """
        self.logger.debug("Entering _shuffle_within_groups.")
        # Define group boundaries
        group_boundaries = {
            "image_inputs": (0, self.PARAMETER_GROUPS["image_inputs"]),
            "double_blocks": (
                self.PARAMETER_GROUPS["image_inputs"],
                self.PARAMETER_GROUPS["image_inputs"] + self.PARAMETER_GROUPS["double_blocks"]
            ),
            "single_blocks": (
                self.PARAMETER_GROUPS["image_inputs"] + self.PARAMETER_GROUPS["double_blocks"],
                self.PARAMETER_GROUPS["image_inputs"] + self.PARAMETER_GROUPS["double_blocks"] + self.PARAMETER_GROUPS["single_blocks"]
            ),
            "final_layer": (
                self.PARAMETER_GROUPS["image_inputs"] + self.PARAMETER_GROUPS["double_blocks"] + self.PARAMETER_GROUPS["single_blocks"],
                self.TOTAL_PARAMETERS
            )
        }

        # Determine which groups to shuffle
        if only_blocks:
            groups_to_shuffle = ["double_blocks", "single_blocks"]
            self.logger.debug(f"only_blocks=True: Only shuffling block groups {groups_to_shuffle}.")
        else:
            groups_to_shuffle = ["image_inputs", "double_blocks", "single_blocks", "final_layer"]
            self.logger.debug("only_blocks=False: Shuffling all parameter groups.")

        # Shuffle selected groups
        for group in groups_to_shuffle:
            start, end = group_boundaries[group]
            group_values = value_list[start:end]
            self.logger.debug(f"Shuffling group '{group}' with indices [{start}:{end}].")
            random.shuffle(group_values)
            value_list[start:end] = group_values
            self.logger.debug(f"Shuffled group '{group}': {group_values}")

        self.logger.debug("Exiting _shuffle_within_groups.")
        return value_list
