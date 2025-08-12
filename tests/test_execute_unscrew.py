import asyncio
from pathlib import Path
from di_core.api import ExecuteRequest
from di_core.runtime import Runtime

async def _collect_statuses(rt, req):
    events = []
    async for st in rt.execute(req):
        events.append(st)
    return events

def test_unscrew_runs():
    Path("/tmp/di_base.json").unlink(missing_ok=True)
    rt = Runtime()
    rt._dbase.set("screws", {"A1": {"x": 0, "y": 0, "dismantled": True}})
    req = ExecuteRequest(skill_name="Unscrew", instance_id="t1", params={"target_id": "A1", "torque": "5"})
    events = asyncio.run(_collect_statuses(rt, req))
    assert events[0].phase == "QUEUED"
    assert any(e.phase == "COMPLETED" for e in events)
