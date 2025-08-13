from __future__ import annotations

import uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from di_core.api import ExecuteRequest
from di_core.registry import registry
from di_core.runtime import Runtime
from di_core.xml_gateway import xml_router

# register example skill via side-effect
from di_skills.skills import unscrew as _  # noqa: F401

app = FastAPI(title="di.core skill runtime")
app.include_router(xml_router)

runtime = Runtime()


@app.get("/skills")
def list_skills():
    """Return list of registered skill names."""
    return registry.list()


@app.post("/execute")
async def execute(req: ExecuteRequest):
    """Execute a skill and collect all status events."""
    events = []
    async for st in runtime.execute(req):
        events.append(st.dict())
    return {"instance_id": req.instance_id, "events": events}


@app.post("/abort/{instance_id}")
def abort(instance_id: str):
    """Abort a running skill instance."""
    ok = runtime.abort(instance_id)
    return {"aborted": ok}


@app.websocket("/ws/execute")
async def ws_execute(ws: WebSocket):
    await ws.accept()
    try:
        data = await ws.receive_json()
        if "instance_id" not in data:
            data["instance_id"] = str(uuid.uuid4())
        req = ExecuteRequest(**data)
        async for st in runtime.execute(req):
            await ws.send_json(st.dict())
    except WebSocketDisconnect:
        pass
    finally:
        await ws.close()
