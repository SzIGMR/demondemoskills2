from __future__ import annotations

import uuid
import xml.etree.ElementTree as ET
from fastapi import APIRouter, Body, Response

from di_core.api import ExecuteRequest
from di_core.runtime import Runtime

# local runtime for XML commands
_runtime = Runtime()

xml_router = APIRouter(prefix="/xml")


@xml_router.post("/command")
async def xml_command(payload: str = Body(..., media_type="application/xml")):
    root = ET.fromstring(payload)
    skill = root.attrib.get("skill", "")
    instance_id = root.attrib.get("instanceId") or str(uuid.uuid4())
    params: dict[str, str] = {}
    for p in root.findall("Param"):
        name = p.attrib.get("name")
        value = p.attrib.get("value", "")
        if name:
            params[name] = value
    req = ExecuteRequest(skill_name=skill, instance_id=instance_id, params=params)
    events = []
    async for st in _runtime.execute(req):
        events.append(st)
    status = ET.Element("DiMontaStatus")
    inst = ET.SubElement(status, "Instance")
    inst.text = instance_id
    for e in events:
        ev = ET.SubElement(status, "Event", phase=e.phase, progress=str(e.progress_pct))
        ev.text = e.message
    xml_resp = ET.tostring(status, encoding="utf-8").decode()
    return Response(content=xml_resp, media_type="application/xml")
