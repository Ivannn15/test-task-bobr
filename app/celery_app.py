import os

from celery import Celery

CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL", "amqp://tasker:tasker@rabbit:5672//"
)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "rpc://")

celery_app = Celery(
    "app",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["app.tasks"],
)
celery_app.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_soft_time_limit=15,
    task_time_limit=20,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
)
