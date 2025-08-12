from __future__ import annotations
import asyncio
from typing import Dict, Callable
from pydantic import BaseModel
from di_core.api import ExecuteStatus
from di_core.registry import registry


class SkillContext(BaseModel):
    instance_id: str
    dbase: object
    emit: Callable[[ExecuteStatus], None]

    class Config:
        arbitrary_types_allowed = True

    async def status(self, message: str, progress: int):
        st = ExecuteStatus(instance_id=self.instance_id, phase="RUNNING", message=message, progress_pct=progress)
        self.emit(st)
        await asyncio.sleep(0)


class Skill:
    NAME: str = "Skill"
    VERSION: str = "0.1.0"

    async def precheck(self, ctx: SkillContext, params: Dict[str, str]) -> None:  # noqa: D401
        """Override to implement safety/availability checks."""
        return None

    async def execute(self, ctx: SkillContext, params: Dict[str, str]) -> Dict[str, str]:  # noqa: D401
        """Override to perform the skill. Must return outputs as dict of strings."""
        raise NotImplementedError


# decorator for registration
def register(cls):
    registry.register(cls)
    return cls
