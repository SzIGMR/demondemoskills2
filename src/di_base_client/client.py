class DiBaseClient:
    def __init__(self) -> None:
        self._storage: dict[str, dict] = {}

    def set(self, key: str, value):
        self._storage[key] = value

    def get(self, key: str, default=None):
        return self._storage.get(key, default)

    def log_result(self, instance_id: str, outputs: dict):
        self.set(instance_id, outputs)
        print(f"[di.base] {instance_id} -> {outputs}")
