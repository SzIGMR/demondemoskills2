from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Dict, Literal


class ExecuteRequest(BaseModel):
    skill_name: str
    instance_id: str
    params: Dict[str, str] = Field(default_factory=dict)


Phase = Literal["QUEUED", "RUNNING", "COMPLETED", "FAILED", "ABORTED"]


class ExecuteStatus(BaseModel):
    instance_id: str
    phase: Phase
    message: str = ""
    progress_pct: int = 0


class ExecuteResult(BaseModel):
    instance_id: str
    success: bool
    outputs: Dict[str, str] = Field(default_factory=dict)
    message: str = ""
