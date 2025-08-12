from __future__ import annotations

import json
from pathlib import Path


class DiBaseClient:
    """Very small persistent key/value store for skills."""

    def __init__(self, path: str | Path = "/tmp/di_base.json") -> None:
        self._path = Path(path)
        if self._path.exists():
            try:
                self._storage: dict[str, dict] = json.loads(self._path.read_text())
            except Exception:  # noqa: BLE001 - best effort load
                self._storage = {}
        else:
            self._storage = {}

    def _save(self) -> None:
        self._path.write_text(json.dumps(self._storage))

    def set(self, key: str, value) -> None:
        self._storage[key] = value
        self._save()

    def get(self, key: str, default=None):
        return self._storage.get(key, default)

    def dump(self) -> dict[str, dict]:
        """Return the entire storage for inspection."""
        return self._storage

    def log_result(self, instance_id: str, outputs: dict) -> None:
        self.set(instance_id, outputs)
        print(f"[di.base] {instance_id} -> {outputs}")
