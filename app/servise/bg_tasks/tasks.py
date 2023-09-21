from app.utils.log import logger
from app.servise.bg_tasks.connect import create_connect_to_celery


celery = create_connect_to_celery()


@celery.task(name=__name__)
def send_to_email_log(message: str) -> None:
    logger.critical(message)
