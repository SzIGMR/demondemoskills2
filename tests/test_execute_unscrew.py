import asyncio
from di_core.api import ExecuteRequest
from di_core.runtime import Runtime

async def _collect_statuses(rt, req):
    events = []
    async for st in rt.execute(req):
        events.append(st)
    return events

def test_unscrew_runs():
    req = ExecuteRequest(skill_name="Unscrew", instance_id="t1", params={"target_id":"A1","torque":"5"})
    rt = Runtime()
    events = asyncio.run(_collect_statuses(rt, req))
    assert events[0].phase == "QUEUED"
    assert any(e.phase == "COMPLETED" for e in events)
