from __future__ import annotations

from di_core.api import Request, Status
from di_core.registry import get


def execute(request: Request) -> Status:
    """Execute a skill based on the request."""
    skill_cls = get(request.name)
    if not skill_cls:
        return Status(success=False, error=f"Skill '{request.name}' not found")

    skill = skill_cls()
    try:
        result = skill.execute(**request.params)
        return Status(success=True, result=result)
    except Exception as exc:  # pragma: no cover - debug path
        return Status(success=False, error=str(exc))
