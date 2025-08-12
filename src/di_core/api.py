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
