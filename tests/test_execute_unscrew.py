import asyncio
import json

import di_skills.skills.unscrew  # noqa: F401 - ensures registration
from di_core.api import ExecuteRequest
from di_core.registry import registry
from di_core.runtime import Runtime


def test_execute_unscrew():
    assert "Unscrew" in registry.list()

    async def run():
        rt = Runtime()
        req = ExecuteRequest(skill_name="Unscrew", instance_id="t1", params={"target_id": "bolt-1"})
        statuses = []
        async for st in rt.execute(req):
            statuses.append(st)
        return statuses

    states = asyncio.run(run())
    assert states[-1].phase == "DONE"
    result = json.loads(states[-1].message)
    assert result["removed"] == "true"
