from __future__ import annotations
from typing import Dict
from di_skills.base import Skill, SkillContext, register

@register
class MySkill(Skill):
    NAME = "MySkill"
    VERSION = "0.1.0"

    async def precheck(self, ctx: SkillContext, params: Dict[str, str]) -> None:
        await ctx.status("precheck ok", 5)

    async def execute(self, ctx: SkillContext, params: Dict[str, str]) -> Dict[str, str]:
        await ctx.status("running", 10)
        # ... do work ...
        return {"ok": "true"}
