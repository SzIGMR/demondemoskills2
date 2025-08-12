from __future__ import annotations

from di_core.registry import registry
from di_skills.base import Skill, SkillContext


@registry.register
class UnscrewSkill(Skill):
    """Simple skill that returns a confirmation output."""

    NAME = "unscrew"

    async def execute(self, ctx: SkillContext, params: dict[str, str]):  # type: ignore[override]
        return {"result": "unscrewed"}
