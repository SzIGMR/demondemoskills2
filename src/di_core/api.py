from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class ExecuteRequest:
    """Request to execute a skill."""

    skill_name: str
    instance_id: str
    params: Dict[str, str]


@dataclass
class ExecuteStatus:
    """Status update emitted during execution."""

    instance_id: str
    phase: str
    message: str
    progress_pct: int
