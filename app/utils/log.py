import logging
from pathlib import Path
from logging.handlers import SMTPHandler

from app.settings.config import SMTPSettings


LOG_FILE = Path().absolute().joinpath("app").joinpath("utils").joinpath("log.log")

formatter = logging.Formatter(style="{", fmt="{asctime} | {levelname} | {message}")

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel("DEBUG")

file_handler = logging.FileHandler(filename=LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)
file_handler.setLevel("DEBUG")

if SMTPSettings().LOGGER_EMAIL and SMTPSettings().LOGGER_PASSWORD:
    smtp_handler = SMTPHandler(
        mailhost=(SMTPSettings().LOGGER_HOST, SMTPSettings().LOGGER_PORT),
        fromaddr=SMTPSettings().LOGGER_EMAIL,
        toaddrs=SMTPSettings().LOGGER_EMAIL,
        subject=SMTPSettings().LOGGER_SUBJECT,
        credentials=(SMTPSettings().LOGGER_EMAIL, SMTPSettings().LOGGER_PASSWORD),
        secure=(),
    )
    smtp_handler.setFormatter(formatter)
    smtp_handler.setLevel("CRITICAL")

    logger.addHandler(smtp_handler)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
