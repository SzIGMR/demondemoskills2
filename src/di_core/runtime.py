from __future__ import annotations

import importlib

from di_core.api import ExecuteRequest, Request, StatusEvent, Status as SyncStatus
from di_core.registry import get
from di_base_client.client import DiBaseClient


def execute(request: Request) -> SyncStatus:
    """Execute a skill based on the request (synchronous API)."""
    skill_cls = get(request.name)
    if not skill_cls:
        return SyncStatus(success=False, error=f"Skill '{request.name}' not found")

    skill = skill_cls()
    try:
        result = skill.execute(**request.params)
        return SyncStatus(success=True, result=result)
    except Exception as exc:  # pragma: no cover - debug path
        return SyncStatus(success=False, error=str(exc))


class Runtime:
    """Minimal asynchronous runtime yielding status events."""

    def __init__(self, client: DiBaseClient | None = None):
        self.client = client or DiBaseClient()

    async def execute(self, request: ExecuteRequest):
        yield StatusEvent(phase="QUEUED")
        name = request.skill_name.lower()
        skill_cls = get(name)
        if not skill_cls:
            try:  # lazy import based on naming convention
                importlib.import_module(f"di_skills.skills.{name}")
                skill_cls = get(name)
            except ModuleNotFoundError:
                skill_cls = None
        if not skill_cls:
            yield StatusEvent(phase="FAILED")
            return
        skill = skill_cls()
        result = skill.execute(**request.params)
        self.client.log_result(request.instance_id, {"result": result})
        yield StatusEvent(phase="COMPLETED")
