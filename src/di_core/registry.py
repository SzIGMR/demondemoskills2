from __future__ import annotations

from typing import Dict, List, Type, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - for type checkers only
    from di_skills.base import Skill


class Registry:
    """Simple in-memory registry for skills."""

    def __init__(self) -> None:
        self._skills: Dict[str, Type["Skill"]] = {}

    def register(self, cls: Type["Skill"]) -> None:
        self._skills[cls.NAME] = cls

    def get(self, name: str):  # type: ignore[return-type]
        return self._skills.get(name)

    def list(self) -> List[str]:
        return sorted(self._skills)


registry = Registry()
