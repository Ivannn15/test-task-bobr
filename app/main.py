from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db, init_db

app = FastAPI(title="Async Task Service")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.post("/tasks", response_model=schemas.TaskCreateResponse, status_code=201)
def create_task(payload_in: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = models.Task(payload=payload_in.payload, status=models.TaskStatus.pending.value)
    db.add(task)
    db.commit()
    db.refresh(task)

    return schemas.TaskCreateResponse(task_id=str(task.id))
