from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseSkill(ABC):
    """Abstract base class for all skills."""

    name: str

    def __init__(self, **context: Any) -> None:
        self.context = context

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Run the skill's logic."""
        raise NotImplementedError
