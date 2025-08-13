import asyncio
from pathlib import Path
from di_core.api import ExecuteRequest
from di_core.runtime import Runtime

PIXEL = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/5+BFQAE/wH+5Jr4GAAAAABJRU5ErkJggg=="

async def _collect_statuses(rt, req):
    events = []
    async for st in rt.execute(req):
        events.append(st)
    return events

def test_detect_screws_from_db():
    Path("/tmp/di_base.json").unlink(missing_ok=True)
    rt = Runtime()
    rt._dbase.set("camera_image", {"format": "png", "data": PIXEL})
    req = ExecuteRequest(skill_name="DetectScrews", instance_id="d1", params={})
    events = asyncio.run(_collect_statuses(rt, req))
    assert any(e.phase == "COMPLETED" for e in events)
    screws = rt._dbase.get("screws")
    assert screws and "S1" in screws
