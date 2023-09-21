from celery import Celery

from app.settings.config import Settings


def create_connect_to_celery() -> Celery:
    celery = Celery(broker=f"redis://{Settings().REDIS_HOST}:{Settings().REDIS_PORT}")
    return celery