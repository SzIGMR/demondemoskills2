from __future__ import annotations
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class DiBaseClient:
    """Stub client that records results."""

    def __init__(self) -> None:
        self.results: Dict[str, Dict[str, str]] = {}

    def log_result(self, instance_id: str, outputs: Dict[str, str]) -> None:
        logger.info("Result %s: %s", instance_id, outputs)
        self.results[instance_id] = outputs
