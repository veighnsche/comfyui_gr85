import random
import yaml


class RandomShowAtmLocOutfit:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {
                    "forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "wildcard": ("STRING", {
                    "default": "shows", "multiline": False}),
                "atmosphere_amount": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "display": "number"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("female_character", "male_character", "random_show", "atmosphere", "location", "outfit")
    FUNCTION = "choose_random_show_atm_loc_outfit"
    CATEGORY = "GR85/Prompt/Wildcard"

    def choose_random_show_atm_loc_outfit(self,
                                          seed,
                                          wildcard,
                                          atmosphere_amount):
        """
        There is a YAML file in the same directory as this file named: shows.yaml
        It contains a list of shows in the following format:
        shows:
          - name: "Show Name"
            charactersFemale:
            - "Character 1"
            charactersMale:
            - "Character 2"
            atmospheres:
            - "Atmosphere 1"
            - "Atmosphere 2"
            locations:
            - "Location 1"
            - "Location 2"
        outfits:
          - "Outfit 1"
          - "Outfit 2"
        """
        with open(f"ComfyUI/custom_nodes/GR85/wildcards/elements/{wildcard}.yaml", "r") as file:
            shows = yaml.load(file, Loader=yaml.FullLoader)
        random.seed(seed)
        show = random.choice(shows['shows'])
        random_show = show['name']
        atmospheres = show['atmospheres']
        locations = show['locations']
        outfits = shows['outfits']
        atmosphere = random.sample(atmospheres, atmosphere_amount)
        location = random.choice(locations)
        outfit = random.choice(outfits)

        female_character = random.choice(show['charactersFemale'])
        male_character = random.choice(show['charactersMale'])

        return female_character, male_character, random_show, ', '.join(atmosphere), location, outfit
