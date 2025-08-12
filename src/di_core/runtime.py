from __future__ import annotations

import asyncio
import json
from typing import AsyncGenerator, Dict

from di_core.api import ExecuteRequest, ExecuteStatus
from di_core.registry import registry
from di_skills.base import SkillContext


class Runtime:
    """Runtime responsible for executing skills asynchronously."""

    def __init__(self) -> None:
        self._tasks: Dict[str, asyncio.Task] = {}

    async def _run(self, req: ExecuteRequest, queue: asyncio.Queue[ExecuteStatus | None]) -> None:
        skill_cls = registry.get(req.skill_name)
        if not skill_cls:
            await queue.put(
                ExecuteStatus(
                    instance_id=req.instance_id,
                    phase="ERROR",
                    message="skill not found",
                    progress_pct=0,
                )
            )
            await queue.put(None)
            return

        ctx = SkillContext(instance_id=req.instance_id, dbase=None, emit=queue.put_nowait)
        skill = skill_cls()
        try:
            await skill.precheck(ctx, req.params)
            outputs = await skill.execute(ctx, req.params)
            await queue.put(
                ExecuteStatus(
                    instance_id=req.instance_id,
                    phase="DONE",
                    message=json.dumps(outputs),
                    progress_pct=100,
                )
            )
        except asyncio.CancelledError:
            await queue.put(
                ExecuteStatus(
                    instance_id=req.instance_id,
                    phase="ABORTED",
                    message="aborted",
                    progress_pct=100,
                )
            )
            raise
        except Exception as exc:  # pragma: no cover - unexpected errors
            await queue.put(
                ExecuteStatus(
                    instance_id=req.instance_id,
                    phase="ERROR",
                    message=str(exc),
                    progress_pct=100,
                )
            )
        finally:
            await queue.put(None)

    async def execute(self, req: ExecuteRequest) -> AsyncGenerator[ExecuteStatus, None]:
        queue: asyncio.Queue[ExecuteStatus | None] = asyncio.Queue()
        task = asyncio.create_task(self._run(req, queue))
        self._tasks[req.instance_id] = task
        try:
            while True:
                st = await queue.get()
                if st is None:
                    break
                yield st
        finally:
            task.cancel()
            self._tasks.pop(req.instance_id, None)

    def abort(self, run_id: str) -> bool:
        task = self._tasks.get(run_id)
        if task and not task.done():
            task.cancel()
            return True
        return False
