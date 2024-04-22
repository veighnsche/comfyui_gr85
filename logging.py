class ShowString:
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "str": ("STRING", {"forceInput": True}),
                "key": ('STRING', {"default": "text"}),
            }
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "show"

    CATEGORY = "GR85/Logging"
    OUTPUT_NODE = True

    def show(self, str, key):
        return {"ui": {key: (str,)}, "result": (str,)}
