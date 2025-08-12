from __future__ import annotations
import asyncio
from typing import Dict
from di_skills.base import Skill, SkillContext, register

@register
class LocateScrew(Skill):
    """Move to a screw and refine its position via camera."""

    NAME = "LocateScrew"
    VERSION = "1.0.0"
    INPUTS = {"screw_id": "Identifier of the screw to localize"}
    OUTPUTS = {"x": "Refined x position", "y": "Refined y position"}

    async def precheck(self, ctx: SkillContext, params: Dict[str, str]) -> None:
        sid = params.get("screw_id")
        screws = ctx.dbase.get("screw_positions", {}) or {}
        if not sid:
            raise ValueError("param 'screw_id' is required")
        if sid not in screws:
            raise ValueError("unknown screw_id")
        await ctx.status("precheck ok", 5)

    async def execute(self, ctx: SkillContext, params: Dict[str, str]) -> Dict[str, str]:
        sid = params["screw_id"]
        screws = ctx.dbase.get("screw_positions", {}) or {}
        coarse = screws[sid]
        await ctx.status(f"move to {sid}", 20)
        await asyncio.sleep(0.1)
        refined = (coarse[0] + 0.5, coarse[1] - 0.2)
        screws[sid] = refined
        ctx.dbase.set("screw_positions", screws)
        await ctx.status("position refined", 90)
        await asyncio.sleep(0.1)
        return {"x": str(refined[0]), "y": str(refined[1])}
