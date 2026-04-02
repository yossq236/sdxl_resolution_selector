from typing import override
from comfy_api.latest import ComfyExtension, io
from .node import SDXLResolutionSelectorNode
from .node2 import SDXLCLIPTextEncodeNode

class MyExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [SDXLResolutionSelectorNode, SDXLCLIPTextEncodeNode]
    @override
    async def on_load(self):
        pass

async def comfy_entrypoint() -> ComfyExtension:
    return MyExtension()

# WEB_DIRECTORY = "./web"
