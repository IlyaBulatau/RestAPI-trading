from fastapi import FastAPI

from app.exeptions.client import handlers as client_handlers
from app.exeptions.client import exeptions as client_exception
from app.exeptions.client import shemas as client_schemes


def setup_exeption_handler(app: FastAPI):
    app.add_exception_handler(
        exc_class_or_status_code=client_exception.TokenException,
        handler=client_handlers.token_exception_handler,
    )
