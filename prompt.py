import random

import openai
import yaml


class RandomTitleCharacter:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {
                    "forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "title_elements_amount": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "display": "number"
                }),
                "character_elements_amount": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "display": "number"
                }),
                "facial_features_amount": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "display": "number"
                }),

            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("random_character", "elements", "facial_features")

    FUNCTION = "choose_random_title_characters"

    CATEGORY = "GR85/Prompt"

    def choose_random_title_characters(self,
                                       seed,
                                       title_elements_amount,
                                       character_elements_amount,
                                       facial_features_amount):
        """
        There is a YAML file in the same directory as this file named: characters.yaml
        It contains a list of characters in the following format:
        - Movie/TV Show/Video Game Title:
        Title_Elements:
            - Title Element
        Characters:
            - Character Name:
            Elements:
                - Character element
            Facial Features:
                - Facial feature

        This function will:
        - Choose a random title
        - Choose a random character from that title
        - Choose 3 random elements from that character
        - Choose a random element from that title

        Returns a string in the following format:
        "Character Name, Title Name, Character element 1, Character element 2, Title Element 1"
        """
        with open("characters.yaml", "r") as file:
            titles = yaml.load(file, Loader=yaml.FullLoader)

        # Use the seed to generate a random number
        random.seed(seed)

        title = random.choice(titles)
        title_name = list(title.keys())[0]
        title_elements = random.sample(title["Title_Elements"], title_elements_amount)

        title_character = random.choice(title["Characters"])
        title_character_name = list(title_character.keys())[0]
        title_character_elements = random.sample(title_character["Elements"], character_elements_amount)

        facial_features = random.sample(title_character["Facial Features"], facial_features_amount)

        return (f"{title_character_name}, {title_name}",
                f"{', '.join(title_character_elements)}, {', '.join(title_elements)}",
                f"{', '.join(facial_features)}")


class InsertCharacter:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "title_character": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "multiline": True,
                }),
                "elements": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "multiline": True
                }),
                "facial_features": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "multiline": True
                }),
                "append": ("STRING", {
                    "default": "",
                    "multiline": True
                }),
                "anime_template": ("STRING", {
                    "default": "1girl, {title_character}, anime, {elements}, {append}",
                    "multiline": True
                }),
                "realistic_template": ("STRING", {
                    "default": "realistic, 1girl, {title_character}, {facial_features}, {elements}, {append}",
                    "multiline": True
                }),
                "face_detailer_template": ("STRING", {
                    "default": "realistic, 1girl, {title_character}, {facial_features}, cute eyes, natural beauty, attractive face, {append}",
                    "multiline": True
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("anime_string", "realistic_string", "face_detailer_string")

    FUNCTION = "insert_character"

    CATEGORY = "GR85/Prompt"

    def insert_character(self, title_character, elements, facial_features, append, anime_template, realistic_template,
                         face_detailer_template):
        """
        This function takes the output of the RandomTitleCharacter node and inserts it into three different templates.
        The templates are strings that contain placeholders for the different elements of the character.
        The placeholders are:
        - {title_character}
        - {elements}
        - {facial_features}
        - {append}

        The function will replace these placeholders with the corresponding elements and return the resulting strings.
        """
        anime = anime_template.format(title_character=title_character, elements=elements,
                                      facial_features=facial_features, append=append)
        realistic = realistic_template.format(title_character=title_character, elements=elements,
                                              facial_features=facial_features, append=append)
        face_detailer = face_detailer_template.format(title_character=title_character, elements=elements,
                                                      facial_features=facial_features, append=append)

        print("Anime:", anime)
        print("Realistic:", realistic)
        print("Face Detailer:", face_detailer)

        return anime, realistic, face_detailer


class RandomElements:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "elements_amount": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "display": "number"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("random_elements",)

    FUNCTION = "choose_random_elements"

    CATEGORY = "GR85/Prompt"

    def choose_random_elements(self, seed, elements_amount):
        with open("elements.yaml", "r") as file:
            elements = yaml.load(file, Loader=yaml.FullLoader)

        result = []
        for element in elements:
            parts = element.split(':')
            if len(parts) == 2:  # Check if we have two parts
                amount_str, name = parts
                amount = int(amount_str)
                result.extend([name] * amount)
            else:
                result.append(element)  # Handle elements without ':'

        random.seed(seed)

        chosen_elements = random.sample(result, elements_amount)

        return (", ".join(chosen_elements),)


class ElementsConcatenator:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "title_character_elements": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "multiline": True
                }),
                "random_elements": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "multiline": True
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("concatenated_elements",)

    FUNCTION = "concatenate_elements"

    CATEGORY = "GR85/Prompt"

    def concatenate_elements(self, title_character_elements, random_elements):
        return (f"{title_character_elements}, {random_elements}",)


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
