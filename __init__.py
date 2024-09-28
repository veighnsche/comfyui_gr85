from custom_nodes.comfyui_gr85.nodes.latent.image_dimension_resizer import ImageDimensionResizer
from custom_nodes.comfyui_gr85.nodes.latent.image_sizer import ImageSizer
from custom_nodes.comfyui_gr85.nodes.latent.image_sizer_all import ImageSizerAll
from custom_nodes.comfyui_gr85.nodes.latent.random_ratio import RandomRatio
from custom_nodes.comfyui_gr85.nodes.logging.show_text import ShowText
from custom_nodes.comfyui_gr85.nodes.mask.batch_rect_mask_generator import BatchRectMaskGenerator
from custom_nodes.comfyui_gr85.nodes.prompt.contains_word import ContainsWord
from custom_nodes.comfyui_gr85.nodes.prompt.element_concatenator import ElementConcatenator
from custom_nodes.comfyui_gr85.nodes.prompt.flux_attention_seeker_2 import FluxAttentionSeeker2
from custom_nodes.comfyui_gr85.nodes.prompt.generate_default_clip_values import GenerateDefaultCLIPValues
from custom_nodes.comfyui_gr85.nodes.prompt.insert_character import InsertCharacter
from custom_nodes.comfyui_gr85.nodes.prompt.int_to_string import IntToStringConverter
from custom_nodes.comfyui_gr85.nodes.prompt.json_file_reader import JSONFileReader
from custom_nodes.comfyui_gr85.nodes.prompt.json_file_saver import JSONFileSaver
from custom_nodes.comfyui_gr85.nodes.prompt.llm_enhance import LlmEnhancer
from custom_nodes.comfyui_gr85.nodes.prompt.string_list_selector import StringListSelector
from custom_nodes.comfyui_gr85.nodes.prompt.tag_injector import TagInjector
from custom_nodes.comfyui_gr85.nodes.prompt.update_clip_blocks import UpdateT5Blocks
from custom_nodes.comfyui_gr85.nodes.prompt.wildcard.random_show_atm_loc_outf import RandomShowAtmLocOutfit
from custom_nodes.comfyui_gr85.nodes.prompt.wildcard.random_title_character import RandomTitleCharacter
from custom_nodes.comfyui_gr85.nodes.prompt.wildcard.random_wildcard_tag_picker import RandomWildcardTagPicker
from custom_nodes.comfyui_gr85.nodes.utils.next_seed import NextSeed
from custom_nodes.comfyui_gr85.nodes.utils.str_safe import StrSafe
from custom_nodes.comfyui_gr85.nodes.mask.paste_by_mask_gr85 import PasteByMaskGr85
from custom_nodes.comfyui_gr85.nodes.prompt.seed_based_output_selector import SeedBasedOutputSelector
from custom_nodes.comfyui_gr85.nodes.prompt.simple_wildcard_picker import SimpleWildcardPicker



NODE_CLASS_MAPPINGS = {
    "GR85_ImageDimensionResizer": ImageDimensionResizer,
    "GR85_ImageSizer": ImageSizer,
    "GR85_ImageSizerAll": ImageSizerAll,
    "GR85_RandomRatio": RandomRatio,

    "GR85_ShowText": ShowText,

    "GR85_RandomTitleCharacter": RandomTitleCharacter,
    "GR85_RandomWildcardTagPicker": RandomWildcardTagPicker,
    "GR85_RandomAtmLocOutfit": RandomShowAtmLocOutfit,

    "GR85_ContainsWord": ContainsWord,
    "GR85_ElementsConcatenator": ElementConcatenator,
    "GR85_InsertCharacter": InsertCharacter,
    "GR85_IntToString": IntToStringConverter,
    "GR85_JSONFileSaver": JSONFileSaver,
    "GR85_JSONFileReader": JSONFileReader,
    "GR85_LlmEnhancer": LlmEnhancer,
    "GR85_TagInjector": TagInjector,
    "GR85_StringListSelector": StringListSelector,
    "GR85_SeedBasedOutputSelector": SeedBasedOutputSelector,
    "GR85_SimpleWildcardPicker": SimpleWildcardPicker,

    "GR85_UpdateT5Blocks": UpdateT5Blocks,
    "GR85_GenerateDefaultClipValues": GenerateDefaultCLIPValues,
    "GR85_FluxAttentionSeeker2": FluxAttentionSeeker2,

    "GR85_NextSeed": NextSeed,
    "GR85_StrSafe": StrSafe,

    "GR85_BatchRectMaskGenerator": BatchRectMaskGenerator,
    "GR85_PasteByMaskGr85": PasteByMaskGr85
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GR85_ImageDimensionResizer": "Image Dimension Resizer",
    "GR85_ImageSizer": "Image Sizer",
    "GR85_ImageSizerAll": "Image Sizer All",
    "GR85_RandomRatio": "Random Ratio",

    "GR85_ShowText": "Show Text",

    "GR85_RandomTitleCharacter": "Random Title Character",
    "GR85_RandomWildcardTagPicker": "Random Wildcard Tag Picker",
    "GR85_RandomAtmLocOutfit": "Random Show Atm Loc Outfit",

    "GR85_ContainsWord": "Contains Word",
    "GR85_ElementsConcatenator": "Elements Concatenator",
    "GR85_InsertCharacter": "Insert Character",
    "GR85_IntToString": "Int To String",
    "GR85_JSONFileSaver": "JSON File Saver",
    "GR85_JSONFileReader": "JSON File Reader",
    "GR85_LlmEnhancer": "Llm Enhancer",
    "GR85_TagInjector": "Tag Injector",
    "GR85_StringListSelector": "String List Selector",
    "GR85_SeedBasedOutputSelector": "Seed Based Output Selector",
    "GR85_SimpleWildcardPicker": "Simple Wildcard Picker",

    "GR85_UpdateT5Blocks": "Update T5 Blocks",
    "GR85_GenerateDefaultClipValues": "Generate Default CLIP Values",
    "GR85_FluxAttentionSeeker2": "Flux Attention Seeker 2",

    "GR85_NextSeed": "Next Seed",
    "GR85_StrSafe": "String Safe",

    "GR85_BatchRectMaskGenerator": "Batch Rect Mask Generator",
    "GR85_PasteByMaskGr85": "Paste By Mask Gr85"
}

WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
