from __future__ import annotations

from di_core.registry import register
from di_skills.base import BaseSkill


class UnscrewSkill(BaseSkill):
    """Simple skill that returns a confirmation string."""

    name = "unscrew"

    def execute(self, **kwargs):  # type: ignore[override]
        return "unscrewed"


register(UnscrewSkill.name, UnscrewSkill)
