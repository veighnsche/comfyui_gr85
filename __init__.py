from typing_extensions import override

from comfy_api.latest import ComfyExtension, io

from .nodes.resolution.image_dimension_resizer import ImageDimensionResizer
from .nodes.resolution.image_sizer import ImageSizer
from .nodes.resolution.image_sizer_all import ImageSizerAll
from .nodes.resolution.random_ratio import RandomRatio
from .nodes.prompt_selection.seed_based_output_selector import SeedBasedOutputSelector
from .nodes.prompt_wildcards.simple_wildcard_picker import SimpleWildcardPicker
from .nodes.prompt_tags.tag_injector import TagInjector, TagInjectorSingle, TagInjectorDuo
from .nodes.prompt_tags.tag_injector_large import TagInjectorLarge
from .nodes.random_seed.next_seed import NextSeed
from .nodes.random_numbers.random_float import RandomFloat
from .nodes.random_numbers.random_int import RandomInt

NODE_CLASS_MAPPINGS = {}

NODE_DISPLAY_NAME_MAPPINGS = {}


class GR85Extension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            SimpleWildcardPicker,
            SeedBasedOutputSelector,
            TagInjectorSingle,
            TagInjectorDuo,
            TagInjector,
            TagInjectorLarge,
            RandomFloat,
            RandomInt,
            NextSeed,
            ImageDimensionResizer,
            ImageSizerAll,
            ImageSizer,
            RandomRatio,
        ]


async def comfy_entrypoint() -> GR85Extension:
    return GR85Extension()

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
