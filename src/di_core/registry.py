from __future__ import annotations
from typing import Dict, Type, List, TYPE_CHECKING

if TYPE_CHECKING:
    from di_skills.base import Skill
else:  # pragma: no cover - used only for typing
    class Skill:  # type: ignore[too-many-ancestors]
        """Runtime placeholder for Skill type."""
        pass

class SkillRegistry:
    def __init__(self) -> None:
        self._skills: Dict[str, Type[Skill]] = {}

    def register(self, cls: Type[Skill]):
        name = getattr(cls, "NAME", cls.__name__)
        self._skills[name] = cls
        return cls

    def get(self, name: str) -> Type[Skill]:
        if name not in self._skills:
            raise KeyError(f"Skill '{name}' not found")
        return self._skills[name]

    def list(self) -> List[str]:
        return sorted(self._skills.keys())

# global registry instance
registry = SkillRegistry()
