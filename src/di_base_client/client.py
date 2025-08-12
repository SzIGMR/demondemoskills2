from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class Client:
    """Stub client that logs messages."""

    def send(self, message: str) -> None:
        logger.info("Client: %s", message)
