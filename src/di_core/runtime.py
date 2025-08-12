from __future__ import annotations
import asyncio
from typing import AsyncIterator, Optional
from di_core.api import ExecuteRequest, ExecuteStatus, ExecuteResult
from di_core.registry import registry
from di_skills.base import SkillContext
from di_base_client.client import DiBaseClient

class Runtime:
    def __init__(self) -> None:
        self._tasks: dict[str, asyncio.Task] = {}
        self._status_queues: dict[str, asyncio.Queue] = {}
        self._dbase = DiBaseClient()

    async def execute(self, req: ExecuteRequest) -> AsyncIterator[ExecuteStatus]:
        # queue for streaming statuses to the caller
        q: asyncio.Queue[ExecuteStatus] = asyncio.Queue()
        self._status_queues[req.instance_id] = q

        await q.put(ExecuteStatus(instance_id=req.instance_id, phase="QUEUED", message="queued", progress_pct=0))

        async def _run():
            try:
                await q.put(ExecuteStatus(instance_id=req.instance_id, phase="RUNNING", message="starting", progress_pct=1))
                skill_cls = registry.get(req.skill_name)
                ctx = SkillContext(instance_id=req.instance_id, dbase=self._dbase, emit=lambda st: q.put_nowait(st))
                skill = skill_cls()
                await skill.precheck(ctx, req.params)
                outputs = await skill.execute(ctx, req.params)
                await q.put(ExecuteStatus(instance_id=req.instance_id, phase="COMPLETED", message="done", progress_pct=100))
                self._dbase.log_result(req.instance_id, outputs)
            except asyncio.CancelledError:
                await q.put(ExecuteStatus(instance_id=req.instance_id, phase="ABORTED", message="aborted", progress_pct=0))
                raise
            except Exception as e:  # noqa: BLE001
                await q.put(ExecuteStatus(instance_id=req.instance_id, phase="FAILED", message=str(e), progress_pct=0))
            finally:
                await asyncio.sleep(0)  # let consumer drain
                q.put_nowait(None)  # sentinel for consumer
                self._status_queues.pop(req.instance_id, None)
                self._tasks.pop(req.instance_id, None)

        task = asyncio.create_task(_run(), name=f"skill-{req.instance_id}")
        self._tasks[req.instance_id] = task

        while True:
            st = await q.get()
            if st is None:  # sentinel
                break
            yield st

    def abort(self, instance_id: str) -> bool:
        t = self._tasks.get(instance_id)
        if t and not t.done():
            t.cancel()
            return True
        return False

    def list_instances(self):
        return list(self._tasks.keys())
