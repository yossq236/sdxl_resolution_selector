from comfy_api.latest import io
from comfy.sd import CLIP
import nodes

class SDXLCLIPTextEncodeNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="SDXLCLIPTextEncodeNode",
            display_name="SDXL CLIPTextEncode",
            category="utils",
            inputs=[
                io.Clip.Input("clip"),
                io.Int.Input("width", default=1024, min=0, max=nodes.MAX_RESOLUTION),
                io.Int.Input("height", default=1024, min=0, max=nodes.MAX_RESOLUTION),
                io.Int.Input("target_width", default=1024, min=0, max=nodes.MAX_RESOLUTION),
                io.Int.Input("target_height", default=1024, min=0, max=nodes.MAX_RESOLUTION),
                io.String.Input("positive", multiline=True, dynamic_prompts=True),
                io.String.Input("negative", multiline=True, dynamic_prompts=True),
                ],
            outputs=[
                io.Conditioning.Output("positive"),
                io.Conditioning.Output("negative"),
                ]
        )

    @classmethod
    def execute(cls, clip, width, height, target_width, target_height, positive, negative) -> io.NodeOutput:
        return io.NodeOutput(
            cls.clip_encode(clip, width, height, 0, 0, target_width, target_height, positive),
            cls.clip_encode(clip, width, height, 0, 0, target_width, target_height, negative),
        )

    @classmethod
    def clip_encode(cls, clip: CLIP, width: int, height: int, crop_w: int, crop_h: int, target_width: int, target_height: int, text: str) -> any:
        tokens = clip.tokenize(text)
        tokens["l"] = clip.tokenize(text)["l"]
        if len(tokens["l"]) != len(tokens["g"]):
            empty = clip.tokenize("")
            while len(tokens["l"]) < len(tokens["g"]):
                tokens["l"] += empty["l"]
            while len(tokens["l"]) > len(tokens["g"]):
                tokens["g"] += empty["g"]
        return clip.encode_from_tokens_scheduled(tokens, add_dict={"width": width, "height": height, "crop_w": crop_w, "crop_h": crop_h, "target_width": target_width, "target_height": target_height})
