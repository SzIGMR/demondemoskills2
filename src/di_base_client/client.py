class DiBaseClient:
    def log_result(self, instance_id: str, outputs: dict):
        print(f"[di.base] {instance_id} -> {outputs}")
