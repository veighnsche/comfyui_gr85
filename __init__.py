from custom_nodes.comfyui_gr85.nodes.latent.image_dimension_resizer import ImageDimensionResizer
from custom_nodes.comfyui_gr85.nodes.latent.image_sizer import ImageSizer
from custom_nodes.comfyui_gr85.nodes.latent.image_sizer_all import ImageSizerAll
from custom_nodes.comfyui_gr85.nodes.latent.random_ratio import RandomRatio
from custom_nodes.comfyui_gr85.nodes.logging.show_text import ShowText
from custom_nodes.comfyui_gr85.nodes.mask.paste_by_mask_gr85 import PasteByMaskGr85
from custom_nodes.comfyui_gr85.nodes.prompt.contains_word import ContainsWord
from custom_nodes.comfyui_gr85.nodes.prompt.flux_attention_seeker_2 import FluxAttentionSeeker2
from custom_nodes.comfyui_gr85.nodes.prompt.flux_attention_seeker_3 import FluxAttentionSeeker3
from custom_nodes.comfyui_gr85.nodes.prompt.flux_attention_seeker_generator import FluxAttentionSeekerGenerator
from custom_nodes.comfyui_gr85.nodes.prompt.int_to_string import IntToStringConverter
from custom_nodes.comfyui_gr85.nodes.prompt.integer_sequence_modifier import IntegerSequenceModifier
from custom_nodes.comfyui_gr85.nodes.prompt.seed_based_output_selector import SeedBasedOutputSelector
from custom_nodes.comfyui_gr85.nodes.prompt.simple_wildcard_picker import SimpleWildcardPicker
from custom_nodes.comfyui_gr85.nodes.prompt.tag_injector import TagInjector
from custom_nodes.comfyui_gr85.nodes.prompt.tag_injector_large import TagInjectorLarge
from custom_nodes.comfyui_gr85.nodes.utils.flux_model_merge_parameters import FluxModelMergeParameters
from custom_nodes.comfyui_gr85.nodes.utils.next_seed import NextSeed
from custom_nodes.comfyui_gr85.nodes.utils.random_float import RandomFloat
from custom_nodes.comfyui_gr85.nodes.utils.random_int import RandomInt
from custom_nodes.comfyui_gr85.nodes.utils.save_text_file import SaveTextFile
from custom_nodes.comfyui_gr85.nodes.utils.save_image_file import SaveImageFile
from custom_nodes.comfyui_gr85.nodes.utils.str_safe import StrSafe

NODE_CLASS_MAPPINGS = {
    "GR85_ImageDimensionResizer": ImageDimensionResizer,
    "GR85_ImageSizer": ImageSizer,
    "GR85_ImageSizerAll": ImageSizerAll,
    "GR85_RandomRatio": RandomRatio,

    "GR85_ShowText": ShowText,

    "GR85_ContainsWord": ContainsWord,
    "GR85_IntToString": IntToStringConverter,
    "GR85_TagInjector": TagInjector,
    "GR85_TagInjectorLarge": TagInjectorLarge,
    "GR85_SeedBasedOutputSelector": SeedBasedOutputSelector,
    "GR85_SimpleWildcardPicker": SimpleWildcardPicker,
    "GR85_IntegerSequenceModifier": IntegerSequenceModifier,

    "GR85_FluxAttentionSeeker2": FluxAttentionSeeker2,
    "GR85_FluxAttentionSeeker3": FluxAttentionSeeker3,
    "GR85_FluxAttentionSeekerGenerator": FluxAttentionSeekerGenerator,
    "GR85_RandomFloat": RandomFloat,
    "GR85_RandomInt": RandomInt,
    "GR85_SaveTextFile": SaveTextFile,
    "GR85_SaveImageFile": SaveImageFile,

    "GR85_FluxModelMergeParameters": FluxModelMergeParameters,
    "GR85_NextSeed": NextSeed,
    "GR85_StrSafe": StrSafe,

    "GR85_PasteByMaskGr85": PasteByMaskGr85
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GR85_ImageDimensionResizer": "Image Dimension Resizer",
    "GR85_ImageSizer": "Image Sizer",
    "GR85_ImageSizerAll": "Image Sizer All",
    "GR85_RandomRatio": "Random Ratio",

    "GR85_ShowText": "Show Text",

    "GR85_ContainsWord": "Contains Word",
    "GR85_IntToString": "Int To String",
    "GR85_TagInjector": "Tag Injector",
    "GR85_TagInjectorLarge": "Tag Injector Large",
    "GR85_SeedBasedOutputSelector": "Seed Based Output Selector",
    "GR85_SimpleWildcardPicker": "Simple Wildcard Picker",
    "GR85_IntegerSequenceModifier": "Integer Sequence Modifier",

    "GR85_FluxAttentionSeeker2": "Flux Attention Seeker 2",
    "GR85_FluxAttentionSeeker3": "Flux Attention Seeker 3",
    "GR85_FluxAttentionSeekerGenerator": "Flux Attention Seeker Generator",
    "GR85_RandomFloat": "Random Float",
    "GR85_RandomInt": "Random Int",
    "GR85_SaveTextFile": "Save Text File",
    "GR85_SaveImageFile": "Save Image File",

    "GR85_FluxModelMergeParameters": "Flux Model Merge Parameters",
    "GR85_NextSeed": "Next Seed",
    "GR85_StrSafe": "String Safe",

    "GR85_PasteByMaskGr85": "Paste By Mask Gr85"
}

WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
