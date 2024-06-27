import re

import openai


def clean_content(content: str) -> str:
    """
    Cleans a string by performing the following:

    * Trims leading/trailing whitespace
    * Replaces line breaks with spaces
    * Collapses multiple spaces into single spaces
    * Removes surrounding quotes if present
    * Removes a trailing period if present

    Args:
        content: The string to be cleaned

    Returns:
        The cleaned string
    """

    # Trim leading/trailing whitespace
    content = content.strip()

    # Replace line endings with spaces
    content = re.sub(r'[\r\n]+', ' ', content)

    # Replace multiple spaces with single spaces
    content = re.sub(r'\s+', ' ', content)

    # Remove surrounding quotes
    if content.startswith('"') and content.endswith('"'):
        content = content[1:-1]

    # Remove trailing period
    if content.endswith('.'):
        content = content[:-1]

    # Trim any remaining whitespace
    content = content.strip()

    return content


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

        try:
            completion = client.chat.completions.create(
                model="Undi95/Xwin-MLewd-13B-V0.2-GGUF",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt.format(title_character=title_character, elements=elements)},
                ],
                temperature=0.7,
            )
            content = clean_content(completion.choices[0].message.content)
            return (content,)
        except Exception as e:
            return (str(e),)
