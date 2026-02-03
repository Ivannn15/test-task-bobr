from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    payload: str = Field(..., min_length=1)


class TaskCreateResponse(BaseModel):
    task_id: str


class TaskRead(BaseModel):
    task_id: str
    payload: str
    status: str
    result: str | None
    created_at: datetime
    updated_at: datetime
