from custom_nodes.GR85.latent import ImageSizer, ImageDimensionResizer
from custom_nodes.GR85.logging import ShowString
from custom_nodes.GR85.prompt import RandomTitleCharacter, InsertCharacter, RandomElements, ElementsConcatenator, \
    LlmEnhancer

NODE_CLASS_MAPPINGS = {
    "GR85_ShowString": ShowString,
    "GR85_ImageSizer": ImageSizer,
    "GR85_ImageDimensionResizer": ImageDimensionResizer,
    "GR85_RandomTitleCharacter": RandomTitleCharacter,
    "GR85_InsertCharacter": InsertCharacter,
    "GR85_RandomElements": RandomElements,
    "GR85_ElementsConcatenator": ElementsConcatenator,
    "GR85_LlmEnhancer": LlmEnhancer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GR85_ShowString": "Show String",
    "GR85_ImageSizer": "Image Sizer",
    "GR85_ImageDimensionResizer": "Image Dimension Resizer",
    "GR85_RandomTitleCharacter": "Random Title Character",
    "GR85_InsertCharacter": "Insert Character",
    "GR85_RandomElements": "Random Elements",
    "GR85_ElementsConcatenator": "Elements Concatenator",
    "GR85_LlmEnhancer": "Llm Enhancer",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
