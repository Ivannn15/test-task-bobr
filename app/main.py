from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db, init_db
from app.tasks import process_task

app = FastAPI(title="Async Task Service")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.post("/tasks", response_model=schemas.TaskCreateResponse, status_code=201)
def create_task(
    payload_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
) -> schemas.TaskCreateResponse:
    task = models.Task(payload=payload_in.payload, status=models.TaskStatus.pending.value)
    db.add(task)
    db.commit()
    db.refresh(task)

    process_task.delay(str(task.id))

    return schemas.TaskCreateResponse(task_id=str(task.id))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks/{task_id}", response_model=schemas.TaskRead)
def get_task(task_id: UUID, db: Session = Depends(get_db)) -> schemas.TaskRead:
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return schemas.TaskRead(
        task_id=str(task.id),
        payload=task.payload,
        status=task.status,
        result=task.result,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
