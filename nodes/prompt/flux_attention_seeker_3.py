import re

class FluxAttentionSeeker3:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "clip": ("CLIP",),
            "apply_to_query": ("BOOLEAN", { "default": True }),
            "apply_to_key": ("BOOLEAN", { "default": True }),
            "apply_to_value": ("BOOLEAN", { "default": True }),
            "apply_to_out": ("BOOLEAN", { "default": True }),
            # Change CLIP layer values to accept a string input
            "clip_l_values_str": ("STRING", {
                "forceInput": True,
                "default": ",".join(["1.0"] * 12),
            }),
            # Change T5 blocks to accept a string input
            "t5xxl_values_str": ("STRING", {
                "forceInput": True,
                "default": ",".join(["1.0"] * 24),
            }),
        }}

    RETURN_TYPES = ("CLIP",)
    FUNCTION = "execute"

    CATEGORY = "GR85/Prompt"

    def execute(self, clip, apply_to_query, apply_to_key, apply_to_value, apply_to_out, clip_l_values_str, t5xxl_values_str):
        if not apply_to_key and not apply_to_query and not apply_to_value and not apply_to_out:
            return (clip, )

        # Parse the t5xxl_values_str into a list of floats
        try:
            t5xxl_values = [float(x.strip()) for x in t5xxl_values_str.split(",")]
        except ValueError:
            raise ValueError("All T5 block values must be valid numbers.")

        # Ensure the correct number of T5 values are provided
        if len(t5xxl_values) != 24:
            raise ValueError(f"Expected 24 T5 block values, but got {len(t5xxl_values)}.")

        # Parse the clip_layer_values_str into a list of floats
        try:
            clip_l_values = [float(x.strip()) for x in clip_l_values_str.split(",")]
        except ValueError:
            raise ValueError("All CLIP layer values must be valid numbers.")

        # Ensure the correct number of CLIP layer values are provided
        if len(clip_l_values) != 12:
            raise ValueError(f"Expected 12 CLIP layer values, but got {len(clip_l_values)}.")

        # Clamp the T5 and CLIP block values to [0, 5]
        t5xxl_values = [max(0.0, min(5.0, v)) for v in t5xxl_values]
        clip_l_values = [max(0.0, min(5.0, v)) for v in clip_l_values]

        m = clip.clone()
        sd = m.patcher.model_state_dict()

        for k in sd:
            if "self_attn" in k:
                # Process CLIP layers
                layer_match = re.search(r"\.layers\.(\d+)\.", k)
                layer = int(layer_match.group(1)) if layer_match else None

                if layer is not None and clip_l_values[layer] != 1.0:
                    if (apply_to_query and "q_proj" in k) or \
                            (apply_to_key and "k_proj" in k) or \
                            (apply_to_value and "v_proj" in k) or \
                            (apply_to_out and "out_proj" in k):
                        m.add_patches({k: (None,)}, 0.0, clip_l_values[layer])
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
