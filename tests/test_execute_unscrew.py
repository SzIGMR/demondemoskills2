from di_core.api import Request
from di_core.registry import list_skills
from di_core.runtime import execute
import di_skills.skills.unscrew  # noqa: F401 - ensures registration


def test_execute_unscrew():
    assert "unscrew" in list_skills()
    request = Request(name="unscrew", params={})
    status = execute(request)
    assert status.success
    assert status.result == "unscrewed"
