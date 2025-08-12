from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Request:
    """Represents a skill execution request."""

    name: str
    params: Dict[str, Any]


@dataclass
class Status:
    """Result of executing a skill."""

    success: bool
    result: Any = None
    error: Optional[str] = None


@dataclass
class ExecuteRequest:
    """Request object for the asynchronous runtime."""

    skill_name: str
    instance_id: str
    params: Dict[str, str]


@dataclass
class StatusEvent:
    """Event yielded during execution."""

    phase: str
