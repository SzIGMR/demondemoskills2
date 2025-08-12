import asyncio
from pathlib import Path
from di_core.api import ExecuteRequest
from di_core.runtime import Runtime


async def _collect_statuses(rt, req):
    events = []
    async for st in rt.execute(req):
        events.append(st)
    return events


def test_bt_workflow_removes_all_screws():
    Path("/tmp/di_base.json").unlink(missing_ok=True)
    rt = Runtime()
    req = ExecuteRequest(
        skill_name="ScrewRemovalWorkflow",
        instance_id="wf1",
        params={"image_path": "img.png"},
    )
    events = asyncio.run(_collect_statuses(rt, req))
    assert any(e.phase == "COMPLETED" for e in events)
    screws = rt._dbase.get("screws")
    assert screws["S1"]["dismantled"] is False
    assert screws["S2"]["dismantled"] is False
    res = rt._dbase.get("wf1")
    assert res and set(res["removed_ids"].split(",")) == {"S1", "S2"}
