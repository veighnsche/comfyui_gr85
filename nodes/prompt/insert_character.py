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
