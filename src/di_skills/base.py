from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass
class SkillContext:
    instance_id: str
    dbase: Any
    emit: Callable[[Any], None]


class Skill(ABC):
    """Base class for asynchronous skills."""

    NAME: str

    async def precheck(self, ctx: SkillContext, params: Dict[str, str]) -> None:
        """Optional pre-execution checks."""
        return None

    @abstractmethod
    async def execute(self, ctx: SkillContext, params: Dict[str, str]) -> Dict[str, str]:
        """Run the skill's logic and return outputs."""
        raise NotImplementedError
