from custom_nodes.GR85.nodes.latent.image_dimension_resizer import ImageDimensionResizer
from custom_nodes.GR85.nodes.latent.image_sizer import ImageSizer
from custom_nodes.GR85.nodes.logging.show_text import ShowText
from custom_nodes.GR85.nodes.prompt.element_concatenator import ElementConcatenator
from custom_nodes.GR85.nodes.prompt.insert_character import InsertCharacter
from custom_nodes.GR85.nodes.prompt.llm_enhance import LlmEnhancer
from custom_nodes.GR85.nodes.prompt.wildcard.random_elements import RandomElements
from custom_nodes.GR85.nodes.prompt.wildcard.random_title_character import RandomTitleCharacter

NODE_CLASS_MAPPINGS = {
    "GR85_ShowText": ShowText,
    "GR85_ImageSizer": ImageSizer,
    "GR85_ImageDimensionResizer": ImageDimensionResizer,
    "GR85_RandomTitleCharacter": RandomTitleCharacter,
    "GR85_InsertCharacter": InsertCharacter,
    "GR85_RandomElements": RandomElements,
    "GR85_ElementsConcatenator": ElementConcatenator,
    "GR85_LlmEnhancer": LlmEnhancer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GR85_ShowText": "Show Text",
    "GR85_ImageSizer": "Image Sizer",
    "GR85_ImageDimensionResizer": "Image Dimension Resizer",
    "GR85_RandomTitleCharacter": "Random Title Character",
    "GR85_InsertCharacter": "Insert Character",
    "GR85_RandomElements": "Random Elements",
    "GR85_ElementsConcatenator": "Elements Concatenator",
    "GR85_LlmEnhancer": "Llm Enhancer",
}

WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
