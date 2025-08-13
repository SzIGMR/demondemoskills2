from __future__ import annotations
import asyncio
import base64
from typing import Dict
from di_skills.base import Skill, SkillContext, register

try:  # pragma: no cover - optional hardware libraries
    import pyrealsense2 as rs  # type: ignore
    import numpy as np
    import cv2
except Exception:  # noqa: BLE001
    rs = None  # type: ignore
    np = None  # type: ignore
    cv2 = None  # type: ignore


PIXEL = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/5+BFQAE/wH+5Jr4GAAAAABJRU5ErkJggg=="
)


@register
class CaptureRealSenseImage(Skill):
    """Capture an image from an Intel RealSense camera and store it in the database."""

    NAME = "CaptureRealSenseImage"
    VERSION = "1.1.0"
    INPUTS: Dict[str, str] = {
        "use_camera": "Set to 'true' to read from a RealSense camera, otherwise a dummy image is stored",
    }
    OUTPUTS = {"image_key": "Database key where the image is stored"}

    async def precheck(self, ctx: SkillContext, params: Dict[str, str]) -> None:
        if params.get("use_camera", "false").lower() != "true":
            await ctx.status("using dummy image", 5)
            return
        if rs is None or np is None or cv2 is None:  # pragma: no cover - import check
            raise RuntimeError(
                "pyrealsense2 and opencv-python are required to capture images"
            )
        await ctx.status("camera ready", 5)

    async def execute(self, ctx: SkillContext, params: Dict[str, str]) -> Dict[str, str]:  # pragma: no cover - hardware interaction
        if params.get("use_camera", "false").lower() == "true" and rs and np and cv2:
            pipeline = rs.pipeline()
            config = rs.config()
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
            pipeline.start(config)
            try:
                frames = pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                image = np.asanyarray(color_frame.get_data())
            finally:
                pipeline.stop()
            _, buf = cv2.imencode(".png", image)
            data_b64 = base64.b64encode(buf.tobytes()).decode()
        else:
            data_b64 = PIXEL
        ctx.dbase.set("camera_image", {"format": "png", "data": data_b64})
        await ctx.status("image captured", 95)
        await asyncio.sleep(0.1)
        return {"image_key": "camera_image"}
