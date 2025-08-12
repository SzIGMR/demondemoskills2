from __future__ import annotations

from di_skills.base import BaseSkill


class SkillTemplate(BaseSkill):
    """Template for new skills."""

    name = "template"

    def execute(self, **kwargs):  # pragma: no cover - template
        raise NotImplementedError
