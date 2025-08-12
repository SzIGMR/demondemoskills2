import asyncio
from pathlib import Path
from di_core.api import ExecuteRequest
from di_core.runtime import Runtime


async def _collect_statuses(rt, req):
    events = []
    async for st in rt.execute(req):
        events.append(st)
    return events


def test_full_workflow():
    Path("/tmp/di_base.json").unlink(missing_ok=True)
    rt = Runtime()
    # detect screws
    req1 = ExecuteRequest(skill_name="DetectScrews", instance_id="d1", params={"image_path": "img.png"})
    asyncio.run(_collect_statuses(rt, req1))
    screws = rt._dbase.get("screws")
    assert screws and "S1" in screws and screws["S1"]["dismantled"]

    # refine position for S1
    req2 = ExecuteRequest(skill_name="LocateScrew", instance_id="l1", params={"screw_id": "S1"})
    asyncio.run(_collect_statuses(rt, req2))
    refined = rt._dbase.get("screws")["S1"]
    assert isinstance(refined, dict) and refined["dismantled"]

    # unscrew S1
    req3 = ExecuteRequest(skill_name="Unscrew", instance_id="u1", params={"target_id": "S1", "torque": "5"})
    events = asyncio.run(_collect_statuses(rt, req3))
    assert any(e.phase == "COMPLETED" for e in events)
    assert not rt._dbase.get("screws")["S1"]["dismantled"]

    # planner should now only return remaining screws
    req4 = ExecuteRequest(skill_name="DismantlingPlanner", instance_id="p1", params={})
    res_events = asyncio.run(_collect_statuses(rt, req4))
    plan = rt._dbase.get("p1")["plan"].split(",") if rt._dbase.get("p1") else []
    assert "S1" not in plan and "S2" in plan
