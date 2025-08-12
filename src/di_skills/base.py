from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Type


class BaseSkill(ABC):
    """Abstract base class for all skills."""

    name: str

    def __init__(self, **context: Any) -> None:
        self.context = context

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Run the skill's logic."""
        raise NotImplementedError


@dataclass
class SkillContext:
    """Runtime-provided context for skill execution."""

    instance_id: str

    async def status(self, message: str, progress: int) -> None:
        """Report intermediate status back to the runtime.

        In this minimal implementation the information is ignored, but the
        method is provided so template skills can await it.
        """
        return None


class Skill(ABC):
    """Asynchronous skill interface used by the templates."""

    NAME: str
    VERSION: str

    async def precheck(self, ctx: SkillContext, params: Dict[str, str]) -> None:
        """Run optional pre-execution checks."""

    async def execute(self, ctx: SkillContext, params: Dict[str, str]) -> Dict[str, str]:
        """Execute the skill and return result parameters."""
        raise NotImplementedError


def register(cls: Type[Skill]) -> Type[Skill]:
    """Class decorator to register a skill by its ``NAME`` attribute."""
    from di_core.registry import register as _register

    _register(cls.NAME.lower(), cls)
    return cls

