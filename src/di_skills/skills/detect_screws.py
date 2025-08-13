from __future__ import annotations
import asyncio
import base64
from typing import Dict
from di_skills.base import Skill, SkillContext, register

try:  # pragma: no cover - optional model libraries
    from ultralytics import YOLO  # type: ignore
    import cv2
    import numpy as np
except Exception:  # noqa: BLE001
    YOLO = None  # type: ignore
    cv2 = None  # type: ignore
    np = None  # type: ignore


@register
class DetectScrews(Skill):
    """Detect screws in an image and store their positions."""

    NAME = "DetectScrews"
    VERSION = "1.2.0"
    INPUTS = {
        "image_path": "Path to the camera image (optional if image is stored in db)",
        "model_path": "Optional path to a YOLOv8 model",
        "use_model": "Set to 'true' to run a YOLOv8 model, otherwise a simulated detection is returned",
    }
    OUTPUTS = {"screw_ids": "Comma separated screw identifiers"}

    async def precheck(self, ctx: SkillContext, params: Dict[str, str]) -> None:
        if not params.get("image_path") and not ctx.dbase.get("camera_image"):
            raise ValueError("image_path param or database image is required")
        if params.get("use_model", "false").lower() == "true":
            if YOLO is None or cv2 is None or np is None:
                raise RuntimeError(
                    "ultralytics, opencv-python and numpy are required to run YOLO models"
                )
        await ctx.status("image received", 5)

    async def execute(self, ctx: SkillContext, params: Dict[str, str]) -> Dict[str, str]:
        await ctx.status("processing image", 20)
        await asyncio.sleep(0.1)
        image = None
        if params.get("image_path") and cv2 is not None:
            image = cv2.imread(params["image_path"])
        elif cv2 is not None and np is not None:
            entry = ctx.dbase.get("camera_image")
            if entry:
                data = base64.b64decode(entry.get("data", ""))
                image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

        use_model = params.get("use_model", "false").lower() == "true"
        screws: Dict[str, Dict[str, float | bool]]
        if image is not None and use_model and YOLO is not None:
            model = YOLO(params.get("model_path", "yolov8n.pt"))
            results = model(image)
            screws = {}
            boxes = results[0].boxes.xyxy.tolist() if results else []
            for i, box in enumerate(boxes, start=1):
                x_center = (box[0] + box[2]) / 2.0
                y_center = (box[1] + box[3]) / 2.0
                screws[f"S{i}"] = {"x": float(x_center), "y": float(y_center), "dismantled": True}
        else:
            # simulated detection result when model or image not available
            screws = {
                "S1": {"x": 10.0, "y": 20.0, "dismantled": True},
                "S2": {"x": 30.0, "y": 40.0, "dismantled": True},
            }
        ctx.dbase.set("screws", screws)
        await ctx.status("screws detected", 90)
        await asyncio.sleep(0.1)
        return {"screw_ids": ",".join(screws.keys())}
