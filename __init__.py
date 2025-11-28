from typing_extensions import override

from comfy_api.latest import ComfyExtension, io

from custom_nodes.comfyui_gr85.nodes.resolution.image_dimension_resizer import ImageDimensionResizer
from custom_nodes.comfyui_gr85.nodes.resolution.image_sizer import ImageSizer
from custom_nodes.comfyui_gr85.nodes.resolution.image_sizer_all import ImageSizerAll
from custom_nodes.comfyui_gr85.nodes.resolution.random_ratio import RandomRatio
from custom_nodes.comfyui_gr85.nodes.prompt_selection.seed_based_output_selector import SeedBasedOutputSelector
from custom_nodes.comfyui_gr85.nodes.prompt_wildcards.simple_wildcard_picker import SimpleWildcardPicker
from custom_nodes.comfyui_gr85.nodes.prompt_tags.tag_injector import TagInjector
from custom_nodes.comfyui_gr85.nodes.prompt_tags.tag_injector import TagInjectorSingle
from custom_nodes.comfyui_gr85.nodes.prompt_tags.tag_injector import TagInjectorDuo
from custom_nodes.comfyui_gr85.nodes.prompt_tags.tag_injector_large import TagInjectorLarge
from custom_nodes.comfyui_gr85.nodes.random_seed.next_seed import NextSeed
from custom_nodes.comfyui_gr85.nodes.random_numbers.random_float import RandomFloat
from custom_nodes.comfyui_gr85.nodes.random_numbers.random_int import RandomInt

NODE_CLASS_MAPPINGS = {
    "GR85_ImageDimensionResizer": ImageDimensionResizer,
    "GR85_ImageSizer": ImageSizer,
    "GR85_ImageSizerAll": ImageSizerAll,
    "GR85_RandomRatio": RandomRatio,

    "GR85_SeedBasedOutputSelector": SeedBasedOutputSelector,
    "GR85_TagInjector": TagInjector,
    "GR85_TagInjectorSingle": TagInjectorSingle,
    "GR85_TagInjectorDuo": TagInjectorDuo,
    "GR85_TagInjectorLarge": TagInjectorLarge,

    "GR85_RandomFloat": RandomFloat,
    "GR85_RandomInt": RandomInt,

    "GR85_NextSeed": NextSeed,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GR85_ImageDimensionResizer": "Image Dimension Resizer",
    "GR85_ImageSizer": "Image Sizer",
    "GR85_ImageSizerAll": "Image Sizer All",
    "GR85_RandomRatio": "Random Ratio",

    "GR85_SeedBasedOutputSelector": "Seed Based Output Selector",
    "GR85_TagInjector": "Tag Injector",
    "GR85_TagInjectorSingle": "Tag Injector Single",
    "GR85_TagInjectorDuo": "Tag Injector Duo",
    "GR85_TagInjectorLarge": "Tag Injector Large",

    "GR85_RandomFloat": "Random Float",
    "GR85_RandomInt": "Random Int",

    "GR85_NextSeed": "Next Seed",
}


class GR85Extension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            SimpleWildcardPicker,
        ]


async def comfy_entrypoint() -> GR85Extension:
    return GR85Extension()

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
