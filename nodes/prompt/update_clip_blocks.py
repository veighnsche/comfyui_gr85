class UpdateT5Blocks:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "t5_values_str": ("STRING", {
                    "forceInput": True,
                    "default": ",".join(["1.0"] * 24),
                }),
                "block_index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 23,
                }),
                "score_adjusted": ("FLOAT", {
                    "default": 0.0,
                    "min": -3.0,
                    "max": 3.0,
                }),
                "score_baseline": ("FLOAT", {
                    "default": 0.0,
                    "min": -3.0,
                    "max": 3.0,
                }),
                "negative_score_adjusted": ("FLOAT", {
                    "default": 0.0,
                    "min": -3.0,
                    "max": 3.0,
                }),
                "negative_score_baseline": ("FLOAT", {
                    "default": 0.0,
                    "min": -3.0,
                    "max": 3.0,
                }),
                "interrogate_score_adjusted": ("INT", {
                    "default": 0,
                    "min": -10,
                    "max": 10,
                }),
                "interrogate_score_baseline": ("INT", {
                    "default": 0,
                    "min": -10,
                    "max": 10,
                }),
                "learning_rate": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "adjusted_value": ("FLOAT", {
                    "default": 1.5,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.01,
                }),
                "positive_weight": ("FLOAT", {
                    "default": 0.4,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "negative_weight": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "interrogate_weight": ("FLOAT", {
                    "default": 0.4,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("updated_t5_values_str",)

    FUNCTION = "update_t5_blocks"

    CATEGORY = "GR85/Prompt"

    def update_t5_blocks(self, t5_values_str, block_index, score_adjusted, score_baseline,
                         negative_score_adjusted, negative_score_baseline,
                         interrogate_score_adjusted, interrogate_score_baseline,
                         learning_rate, adjusted_value,
                         positive_weight, negative_weight, interrogate_weight):
        """
        Updates the T5 block values based on the change in desirability.

        Parameters:
            t5_values_str (str): Comma-separated string of 24 float values.
            block_index (int): Index of the T5 block to adjust (0-23).
            score_adjusted (float): Positive score with the adjusted T5 block.
            score_baseline (float): Positive score with the baseline T5 blocks.
            negative_score_adjusted (float): Negative score with the adjusted T5 block.
            negative_score_baseline (float): Negative score with the baseline T5 blocks.
            interrogate_score_adjusted (float): Interrogate score with the adjusted T5 block.
            interrogate_score_baseline (float): Interrogate score with the baseline T5 blocks.
            learning_rate (float): The rate at which the T5 block values are adjusted.
            adjusted_value (float): The target adjusted value for the T5 block.
            positive_weight (float): Weight of the positive desirability.
            negative_weight (float): Weight of the negative desirability.
            interrogate_weight (float): Weight of the interrogate desirability.

        Returns:
            tuple: Updated comma-separated string of T5 block values.
        """
        # Normalize weights
        total_weight = positive_weight + negative_weight + interrogate_weight
        if total_weight == 0:
            raise ValueError("The sum of the weights must be greater than zero.")
        positive_weight /= total_weight
        negative_weight /= total_weight
        interrogate_weight /= total_weight

        # Convert the input string to a list of floats
        try:
            t5_values = [float(x.strip()) for x in t5_values_str.split(",")]
        except ValueError:
            raise ValueError("All T5 block values must be valid numbers.")

        # Ensure the list has exactly 24 elements
        if len(t5_values) != 24:
            raise ValueError(f"Expected 24 T5 block values, but got {len(t5_values)}.")

        # Ensure block_index is an integer within valid range
        if not isinstance(block_index, int):
            raise TypeError("Block index must be an integer.")
        if not (0 <= block_index < 24):
            raise ValueError(f"Block index out of range (0-23): {block_index}.")

        # Clamp scores to [-3, 3] for positive and negative scores
        score_adjusted = max(-3.0, min(3.0, score_adjusted))
        score_baseline = max(-3.0, min(3.0, score_baseline))
        negative_score_adjusted = max(-3.0, min(3.0, negative_score_adjusted))
        negative_score_baseline = max(-3.0, min(3.0, negative_score_baseline))

        # Normalize interrogate scores from [-10, 10] to [-3, 3]
        def normalize_interrogate_score(score):
            return (score / 10.0) * 3.0

        interrogate_score_adjusted = max(-10.0, min(10.0, interrogate_score_adjusted))
        interrogate_score_baseline = max(-10.0, min(10.0, interrogate_score_baseline))

        normalized_interrogate_score_adjusted = normalize_interrogate_score(interrogate_score_adjusted)
        normalized_interrogate_score_baseline = normalize_interrogate_score(interrogate_score_baseline)

        # Normalize scores to desirabilities between 0 and 1
        desirability_positive_adjusted = (score_adjusted + 3) / 6
        desirability_positive_baseline = (score_baseline + 3) / 6
        desirability_negative_adjusted = (negative_score_adjusted + 3) / 6
        desirability_negative_baseline = (negative_score_baseline + 3) / 6
        desirability_interrogate_adjusted = (normalized_interrogate_score_adjusted + 3) / 6
        desirability_interrogate_baseline = (normalized_interrogate_score_baseline + 3) / 6

        # Weighted average for overall desirabilities
        overall_desirability_adjusted = (
                positive_weight * desirability_positive_adjusted +
                negative_weight * desirability_negative_adjusted +
                interrogate_weight * desirability_interrogate_adjusted
        )
        overall_desirability_baseline = (
                positive_weight * desirability_positive_baseline +
                negative_weight * desirability_negative_baseline +
                interrogate_weight * desirability_interrogate_baseline
        )

        # Calculate the change in desirability
        delta_desirability = overall_desirability_adjusted - overall_desirability_baseline

        # Introduce the learning rate to scale the change
        delta_desirability *= learning_rate

        # Calculate the change in value
        current_value = t5_values[block_index]
        delta_value = adjusted_value - current_value

        # Update the T5 block value
        new_value = current_value + delta_value * delta_desirability

        # Ensure the new value is within [0, 5]
        new_value = max(0.0, min(5.0, new_value))

        # Update the list
        t5_values[block_index] = new_value

        # Convert the list back to a string without spaces
        updated_t5_values_str = ",".join(f"{v:.4f}" for v in t5_values)

        return (updated_t5_values_str,)
