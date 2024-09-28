from random import Random
import re


class SimpleWildcardPicker:
    def __init__(self):
        pass

    """
    ComfyUI Custom Node
    Implements wildcards using a seed for reproducibility.
    """

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Prompt String",)
    OUTPUT_NODE = False
    FUNCTION = "process_wildcards"

    CATEGORY = "GR85/Prompt"

    WILDCARD_PATTERN = re.compile(r'{[^{}]+}')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ('STRING', {'default': '', 'multiline': True, 'dynamicPrompts': False}),
                "seed": ('INT', {'default': 0, 'min': 0, 'max': 2147483647})
            }
        }

    @staticmethod
    def process_wildcards(prompt, seed):
        """
        Process wildcards using a seed to produce stable output, with support for nested wildcards.
        """
        rng = Random(seed)

        def replace_nested_wildcards(p):
            # Base case: no wildcards left
            if '{' not in p:
                return p

            result = ''
            i = 0
            while i < len(p):
                if p[i] == '{':
                    # Find the matching closing brace
                    depth = 1
                    j = i + 1
                    while j < len(p) and depth > 0:
                        if p[j] == '{':
                            depth += 1
                        elif p[j] == '}':
                            depth -= 1
                        j += 1
                    if depth == 0:
                        # Extract the content inside the braces
                        content = p[i + 1:j - 1]
                        if not content:
                            raise ValueError(f"Empty wildcard found at position {i}.")
                        # Recursively replace nested wildcards in content
                        replaced_content = replace_nested_wildcards(content)
                        # Split options and pick one
                        options = replaced_content.split('|')
                        if not options:
                            raise ValueError(f"No options found in wildcard at position {i}.")
                        picked_option = options[rng.randint(0, len(options) - 1)]
                        # Add to result
                        result += picked_option
                        i = j
                    else:
                        # Unmatched opening brace
                        raise ValueError(f"Unmatched opening brace at position {i}.")
                elif p[i] == '}':
                    # Unmatched closing brace
                    raise ValueError(f"Unmatched closing brace at position {i}.")
                else:
                    result += p[i]
                    i += 1
            return result

        try:
            prompt = replace_nested_wildcards(prompt)
        except ValueError as e:
            # Handle errors (could log or re-raise)
            print(f"Error processing prompt: {e}")
            prompt = ''  # Or handle as appropriate

        return prompt

