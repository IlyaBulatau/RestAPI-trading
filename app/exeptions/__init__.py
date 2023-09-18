from fastapi import FastAPI

from app.exeptions.client import handlers as hand
from app.exeptions.client import exeptions as exc


def setup_exeption_handler(app: FastAPI):
    app.add_exception_handler(
        exc_class_or_status_code=exc.TokenException,
        handler=hand.token_exception_handler,
    )
