from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    payload: str = Field(..., min_length=1)


class TaskCreateResponse(BaseModel):
    task_id: str
