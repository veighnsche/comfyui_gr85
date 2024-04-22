import random

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

    CATEGORY = "GR85/Prompt/Wildcard"

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
