import openai


class LlmEnhancer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "title_character": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "multiline": True
                }),
                "elements": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "multiline": True
                }),
                "system_prompt": ("STRING", {
                    "default": "Enhance the following elements into a short and simple movie still that is coherent with the character.",
                    "multiline": True
                }),
                "user_prompt": ("STRING", {
                    "default": "Character in scene: {title_character}, Props: {elements}",
                    "multiline": True
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("enhanced_string",)
    FUNCTION = "enhance_string"
    CATEGORY = "GR85/Prompt"

    def enhance_string(self, title_character, elements, system_prompt, user_prompt):
        """
        This makes a call to: http://localhost:7875/v1/chat/completions
        This service is a ChatGPT model that has been fine-tuned to respond with an enhanced version of the input text.
        """
        client = openai.OpenAI(base_url="http://localhost:7875/v1", api_key="lm-studio")

        completion = client.chat.completions.create(
            model="Undi95/Xwin-MLewd-13B-V0.2-GGUF",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt.format(title_character=title_character, elements=elements)},
            ],
            temperature=0.7,
        )

        try:
            return (completion.choices[0].message.content,)
        except Exception as e:
            return (str(e),)
