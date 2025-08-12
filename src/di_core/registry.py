from __future__ import annotations

from typing import Dict, List, Optional, Type

from di_skills.base import BaseSkill

_registry: Dict[str, Type[BaseSkill]] = {}


def register(name: str, skill_cls: Type[BaseSkill]) -> None:
    """Register a skill class under a name."""
    _registry[name] = skill_cls


def get(name: str) -> Optional[Type[BaseSkill]]:
    """Retrieve a skill class by name."""
    return _registry.get(name)


def list_skills() -> List[str]:
    """Return the names of all registered skills."""
    return sorted(_registry)
