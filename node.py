from comfy_api.latest import io
import math

class Resolution:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        gcd = math.gcd(self.width, self.height)
        self.label = "{}x{}({}:{})".format(self.width, self.height, int(self.width // gcd), int(self.height // gcd))

RESOLUTIONS = [
    Resolution(1024, 1024),
    Resolution( 960, 1024),
    Resolution( 960, 1088),
    Resolution( 896, 1088),
    Resolution( 896, 1152),
    Resolution( 832, 1152),
    Resolution( 832, 1216),
    Resolution( 768, 1280),
    Resolution( 768, 1344),
    Resolution( 704, 1344),
    Resolution( 704, 1408),
    Resolution( 704, 1472),
    Resolution( 640, 1536),
    Resolution( 640, 1600),
    Resolution( 576, 1664),
    Resolution( 576, 1728),
    Resolution( 576, 1792),
    Resolution( 512, 1856),
    Resolution( 512, 1920),
    Resolution( 512, 1984),
    Resolution( 512, 2048),
    ]

ORIENTATIONS = [
    "portrait",
    "landscape",
    ]

class SDXLResolutionSelectorNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="SDXLResolutionSelectorNode",
            display_name="SDXL Resolution Selector",
            category="utils",
            inputs=[
                io.Combo.Input("resolution",options=[n.label for n in RESOLUTIONS],default=RESOLUTIONS[0].label),
                io.Combo.Input("orientation",options=ORIENTATIONS,default=ORIENTATIONS[0]),
                io.Float.Input("scale_by",default=1.0,min=0.5,max=9.5),
                ],
            outputs=[
                io.Int.Output("width"),
                io.Int.Output("height"),
                io.Int.Output("target_width"),
                io.Int.Output("target_height"),
                ]
        )

    @classmethod
    def execute(cls, resolution, orientation, scale_by) -> io.NodeOutput:
        selection = next((n for n in RESOLUTIONS if n.label == resolution),None)
        if selection is not None:
            base_w = selection.width
            base_h = selection.height
        else:
            base_w = 1024
            base_h = 1024
        scaled_w = int((base_w * scale_by + 7) // 8 * 8)
        scaled_h = int((base_h * scale_by + 7) // 8 * 8)
        if orientation == "portrait":
            return io.NodeOutput(scaled_w, scaled_h, base_w, base_h)
        else:
            return io.NodeOutput(scaled_h, scaled_w, base_h, base_w)

