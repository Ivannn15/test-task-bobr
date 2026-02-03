import random
import time
import uuid

from app import models
from app.celery_app import celery_app
from app.db import SessionLocal


@celery_app.task(name="tasks.process_task")
def process_task(task_id: str) -> None:
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        return

    db = SessionLocal()
    try:
        task = db.get(models.Task, task_uuid)
        if not task:
            return

        task.status = models.TaskStatus.processing.value
        db.commit()

        time.sleep(random.randint(2, 5))

        task.result = f"Processed payload: {task.payload}"
        task.status = models.TaskStatus.done.value
        db.commit()
    except Exception as exc:
        db.rollback()
        task = db.get(models.Task, task_uuid)
        if task:
            task.status = models.TaskStatus.failed.value
            task.result = str(exc)
            db.commit()
        raise
    finally:
        db.close()
