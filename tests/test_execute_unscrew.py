import pytest
from di_core.api import ExecuteRequest
from di_core.runtime import Runtime
from di_core.registry import registry
import di_skills.skills.unscrew  # noqa: F401 - ensure registration


@pytest.mark.asyncio
async def test_execute_unscrew():
    rt = Runtime()
    req = ExecuteRequest(skill_name="unscrew", instance_id="abc123", params={})

    statuses = [st async for st in rt.execute(req)]
    assert [s.phase for s in statuses] == ["QUEUED", "RUNNING", "COMPLETED"]
    assert registry.list() == ["unscrew"]
    assert rt._dbase.results["abc123"] == {"result": "unscrewed"}
    assert rt.list_instances() == []
