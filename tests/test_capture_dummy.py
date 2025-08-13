import asyncio
from pathlib import Path
from di_core.api import ExecuteRequest
from di_core.runtime import Runtime

async def _collect_statuses(rt, req):
    events = []
    async for st in rt.execute(req):
        events.append(st)
    return events


def test_capture_dummy_image():
    Path("/tmp/di_base.json").unlink(missing_ok=True)
    rt = Runtime()
    req = ExecuteRequest(skill_name="CaptureRealSenseImage", instance_id="c1", params={})
    events = asyncio.run(_collect_statuses(rt, req))
    assert any(e.phase == "COMPLETED" for e in events)
    entry = rt._dbase.get("camera_image")
    assert entry and entry.get("data")
