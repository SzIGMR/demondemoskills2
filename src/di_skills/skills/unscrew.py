from __future__ import annotations
import asyncio
from typing import Dict
from di_skills.base import Skill, SkillContext, register

@register
class Unscrew(Skill):
    """Remove a screw using a preset torque."""

    NAME = "Unscrew"
    VERSION = "1.0.0"
    INPUTS = {"target_id": "ID of the screw to remove", "torque": "Torque in Nm"}
    OUTPUTS = {"removed": "true if screw removed", "time_s": "time taken in seconds"}

    async def precheck(self, ctx: SkillContext, params: Dict[str, str]) -> None:
        target = params.get("target_id", "")
        if not target:
            raise ValueError("param 'target_id' is required")
        await ctx.status(f"precheck ok for {target}", 5)

    async def execute(self, ctx: SkillContext, params: Dict[str, str]) -> Dict[str, str]:
        torque = params.get("torque", "5")
        target = params["target_id"]
        positions = ctx.dbase.get("screw_positions", {}) or {}
        pos = positions.get(target, (0, 0))
        await ctx.status(f"move to {target} at {pos}", 15)
        await asyncio.sleep(0.1)  # simulate motion
        await ctx.status(f"set torque {torque}Nm", 25)
        await asyncio.sleep(0.1)
        # simulated unscrew steps
        for i in range(5):
            await ctx.status(f"unscrewing step {i+1}/5", 40 + i*10)
            await asyncio.sleep(0.1)
        await ctx.status("retract tool", 95)
        await asyncio.sleep(0.1)
        positions.pop(target, None)
        ctx.dbase.set("screw_positions", positions)
        return {"removed": "true", "time_s": "0.7"}
