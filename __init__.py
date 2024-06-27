from nodes.sizes.image_dimension_resizer import ImageDimensionResizer
from nodes.sizes.image_sizer import ImageSizer
from nodes.sizes.random_ratio import RandomRatio
from nodes.logging.show_text import ShowText
from nodes.prompt.contains_word import ContainsWord
from nodes.prompt.element_concatenator import ElementConcatenator
from nodes.prompt.insert_character import InsertCharacter
from nodes.prompt.llm_enhance import LlmEnhancer
from nodes.prompt.tag_injector import TagInjector
from nodes.prompt.wildcard.random_title_character import RandomTitleCharacter
from nodes.prompt.wildcard.random_wildcard_tag_picker import RandomWildcardTagPicker
from nodes.prompt.wildcard.random_show_atm_loc_outf import RandomShowAtmLocOutfit
from nodes.utils.next_seed import NextSeed
from nodes.utils.str_safe import StrSafe

NODE_CLASS_MAPPINGS = {
    "GR85_ImageDimensionResizer": ImageDimensionResizer,
    "GR85_ImageSizer": ImageSizer,
    "GR85_RandomRatio": RandomRatio,

    "GR85_ShowText": ShowText,

    "GR85_RandomTitleCharacter": RandomTitleCharacter,
    "GR85_RandomWildcardTagPicker": RandomWildcardTagPicker,
    "GR85_RandomAtmLocOutfit": RandomShowAtmLocOutfit,

    "GR85_ContainsWord": ContainsWord,
    "GR85_ElementsConcatenator": ElementConcatenator,
    "GR85_InsertCharacter": InsertCharacter,
    "GR85_LlmEnhancer": LlmEnhancer,
    "GR85_TagInjector": TagInjector,

    "GR85_NextSeed": NextSeed,
    "GR85_StrSafe": StrSafe,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GR85_ImageDimensionResizer": "Image Dimension Resizer",
    "GR85_ImageSizer": "Image Sizer",
    "GR85_RandomRatio": "Random Ratio",

    "GR85_ShowText": "Show Text",

    "GR85_RandomTitleCharacter": "Random Title Character",
    "GR85_RandomWildcardTagPicker": "Random Wildcard Tag Picker",
    "GR85_RandomAtmLocOutfit": "Random Show Atm Loc Outfit",

    "GR85_ContainsWord": "Contains Word",
    "GR85_ElementsConcatenator": "Elements Concatenator",
    "GR85_InsertCharacter": "Insert Character",
    "GR85_LlmEnhancer": "Llm Enhancer",
    "GR85_TagInjector": "Tag Injector",

    "GR85_NextSeed": "Next Seed",
    "GR85_StrSafe": "String Safe",
}

WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
