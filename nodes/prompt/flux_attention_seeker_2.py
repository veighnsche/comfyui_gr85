import re

class FluxAttentionSeeker2:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "clip": ("CLIP",),
            "apply_to_query": ("BOOLEAN", { "default": True }),
            "apply_to_key": ("BOOLEAN", { "default": True }),
            "apply_to_value": ("BOOLEAN", { "default": True }),
            "apply_to_out": ("BOOLEAN", { "default": True }),
            # Keep CLIP layer sliders
            **{f"clip_l_{s}": ("FLOAT", {
                "display": "slider",
                "default": 1.0,
                "min": 0,
                "max": 5,
                "step": 0.05
            }) for s in range(12)},
            # Change T5 blocks to accept a string input
            "t5xxl_values_str": ("STRING", {
                "forceInput": True,
                "default": ",".join(["1.0"] * 24),
            }),
        }}

    RETURN_TYPES = ("CLIP",)
    FUNCTION = "execute"

    CATEGORY = "GR85/Prompt"

    def execute(self, clip, apply_to_query, apply_to_key, apply_to_value, apply_to_out, t5xxl_values_str, **values):
        if not apply_to_key and not apply_to_query and not apply_to_value and not apply_to_out:
            return (clip, )

        # Parse the t5xxl_values_str into a list of floats
        try:
            t5xxl_values = [float(x.strip()) for x in t5xxl_values_str.split(",")]
        except ValueError:
            raise ValueError("All T5 block values must be valid numbers.")

        # Ensure the correct number of values are provided
        if len(t5xxl_values) != 24:
            raise ValueError(f"Expected 24 T5 block values, but got {len(t5xxl_values)}.")

        # Clamp the T5 block values to [0, 5]
        t5xxl_values = [max(0.0, min(5.0, v)) for v in t5xxl_values]

        m = clip.clone()
        sd = m.patcher.model_state_dict()

        for k in sd:
            if "self_attn" in k:
                # Process CLIP layers
                layer_match = re.search(r"\.layers\.(\d+)\.", k)
                layer = int(layer_match.group(1)) if layer_match else None

                if layer is not None and values.get(f"clip_l_{layer}", 1.0) != 1.0:
                    if (apply_to_query and "q_proj" in k) or \
                            (apply_to_key and "k_proj" in k) or \
                            (apply_to_value and "v_proj" in k) or \
                            (apply_to_out and "out_proj" in k):
                        m.add_patches({k: (None,)}, 0.0, values[f"clip_l_{layer}"])
            elif "SelfAttention" in k:
                # Process T5 blocks
                block_match = re.search(r"\.block\.(\d+)\.", k)
                block = int(block_match.group(1)) if block_match else None

                if block is not None and t5xxl_values[block] != 1.0:
                    if (apply_to_query and ".q." in k) or \
                            (apply_to_key and ".k." in k) or \
                            (apply_to_value and ".v." in k) or \
                            (apply_to_out and ".o." in k):
                        m.add_patches({k: (None,)}, 0.0, t5xxl_values[block])

        return (m, )
