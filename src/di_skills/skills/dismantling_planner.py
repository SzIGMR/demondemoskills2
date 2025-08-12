from __future__ import annotations
import asyncio
import random
from typing import Dict
from di_skills.base import Skill, SkillContext, register

@register
class DismantlingPlanner(Skill):
    """Plan a random sequence of screws to dismantle."""

    NAME = "DismantlingPlanner"
    VERSION = "1.0.0"
    INPUTS: Dict[str, str] = {}
    OUTPUTS = {"plan": "Comma separated screw identifiers"}

    async def precheck(self, ctx: SkillContext, params: Dict[str, str]) -> None:
        screws = ctx.dbase.get("screws", {}) or {}
        if not screws:
            raise ValueError("no screws available")
        await ctx.status("planning", 5)

    async def execute(self, ctx: SkillContext, params: Dict[str, str]) -> Dict[str, str]:
        await ctx.status("collecting", 20)
        await asyncio.sleep(0.1)
        screws = ctx.dbase.get("screws", {}) or {}
        ids = [sid for sid, info in screws.items() if info.get("dismantled")]
        random.shuffle(ids)
        await ctx.status("plan ready", 90)
        await asyncio.sleep(0.1)
        return {"plan": ",".join(ids)}
