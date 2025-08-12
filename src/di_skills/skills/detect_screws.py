from __future__ import annotations
import asyncio
from typing import Dict
from di_skills.base import Skill, SkillContext, register

@register
class DetectScrews(Skill):
    """Detect screws in an image and store their positions."""

    NAME = "DetectScrews"
    VERSION = "1.0.0"
    INPUTS = {"image_path": "Path to the camera image"}
    OUTPUTS = {"screw_ids": "Comma separated screw identifiers"}

    async def precheck(self, ctx: SkillContext, params: Dict[str, str]) -> None:
        if not params.get("image_path"):
            raise ValueError("param 'image_path' is required")
        await ctx.status("image received", 5)

    async def execute(self, ctx: SkillContext, params: Dict[str, str]) -> Dict[str, str]:
        await ctx.status("processing image", 20)
        await asyncio.sleep(0.1)
        # simulated detection result
        screws = {
            "S1": {"x": 10.0, "y": 20.0, "dismantled": True},
            "S2": {"x": 30.0, "y": 40.0, "dismantled": True},
        }
        ctx.dbase.set("screws", screws)
        await ctx.status("screws detected", 90)
        await asyncio.sleep(0.1)
        return {"screw_ids": ",".join(screws.keys())}
