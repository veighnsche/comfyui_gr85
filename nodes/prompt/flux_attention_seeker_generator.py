import random

class FluxAttentionSeekerGenerator:
    TOTAL_VALUES = 36
    CLIP_VALUES_COUNT = 12
    T5XXL_VALUES_COUNT = 24
    MAX_SEED = 0xffffffffffffffff

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": cls.MAX_SEED,
                    "step": 1,
                    "display": "number"
                }),
                "distribution_scale": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "number"
                }),
                "random_generation_count": ("INT", {
                    "default": cls.TOTAL_VALUES,
                    "min": 0,
                    "max": cls.TOTAL_VALUES,
                    "step": 1,
                    "display": "number"
                })
            },
            "optional": {
                "combined_values": ("STRING", {
                    "forceInput": True
                })
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "FLOAT")
    RETURN_NAMES = ("clip_l_values", "t5xxl_values", "combined_values", "average_value")
    FUNCTION = "execute"
    CATEGORY = "GR85/Prompt"

    def execute(self, seed, distribution_scale=0.5, random_generation_count=36, combined_values=None):
        if not (0 <= distribution_scale <= 1):
            raise ValueError("distribution_scale must be between 0.0 and 1.0.")
        if not (0 <= random_generation_count <= self.TOTAL_VALUES):
            raise ValueError(f"random_generation_count must be between 0 and {self.TOTAL_VALUES}.")
        if not (0 <= seed <= self.MAX_SEED):
            raise ValueError(f"seed must be between 0 and {self.MAX_SEED}.")

        random.seed(seed)

        # Parse combined_values if provided, or initialize all_values to 1.0
        if combined_values:
            try:
                all_values = [float(value) for value in combined_values.split(",")]
                if len(all_values) != self.TOTAL_VALUES:
                    raise ValueError(f"combined_values must contain exactly {self.TOTAL_VALUES} values.")
            except ValueError:
                raise ValueError("All entries in combined_values must be numeric.")
        else:
            # Generate random values within 0 to 2 if combined_values is not provided
            all_values = [1.0] * self.TOTAL_VALUES
            modified_values = [
                max(0.0, min(2.0, round(random.gauss(1.0, 0.5 * distribution_scale), 4)))
                for _ in range(random_generation_count)
            ]
            # Assign and shuffle modified values within all_values
            all_values[:random_generation_count] = modified_values
            random.shuffle(all_values)

        # Prepare output strings and calculate average
        clip_l_values_str = ",".join(map(str, all_values[:self.CLIP_VALUES_COUNT]))
        t5xxl_values_str = ",".join(map(str, all_values[self.CLIP_VALUES_COUNT:]))
        combined_values_str = ",".join(map(str, all_values))
        average_value = round(sum(all_values) / len(all_values), 10)

        return (clip_l_values_str, t5xxl_values_str, combined_values_str, average_value)
