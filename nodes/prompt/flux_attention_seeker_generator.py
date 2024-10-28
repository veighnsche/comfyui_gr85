import random

class FluxAttentionSeekerGenerator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,  # Maximum 64-bit unsigned integer
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

    def execute(self, seed, combined_values=None):
        random.seed(seed)

        if combined_values:
            values = combined_values.split(",")
            if len(values) != 36:
                raise ValueError("combined_values must contain 36 comma-separated values.")
            clip_l_values_str = ",".join(values[:12])
            t5xxl_values_str = ",".join(values[12:])
            combined_values_str = combined_values
            all_values = list(map(float, values))
        else:
            # Generate random values for CLIP layers (12 values with normal distribution centered at 1)
            clip_l_values = [round(random.gauss(1, 0.5), 2) for _ in range(12)]
            clip_l_values = [max(0, min(2, v)) for v in clip_l_values]  # Clamp values between 0 and 2
            clip_l_values_str = ",".join(map(str, clip_l_values))

            # Generate random values for T5 blocks (24 values with normal distribution centered at 1)
            t5xxl_values = [round(random.gauss(1, 0.5), 2) for _ in range(24)]
            t5xxl_values = [max(0, min(2, v)) for v in t5xxl_values]  # Clamp values between 0 and 2
            t5xxl_values_str = ",".join(map(str, t5xxl_values))

            combined_values_str = clip_l_values_str + "," + t5xxl_values_str
            all_values = clip_l_values + t5xxl_values

        average_value = round(sum(all_values) / len(all_values), 10)

        return (clip_l_values_str, t5xxl_values_str, combined_values_str, average_value)
