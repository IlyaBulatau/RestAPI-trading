from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, ValidationException

from app.exeptions.client import handlers as client_handlers
from app.exeptions.client import exeptions as client_exception
from app.exeptions.client import shemas as client_schemes

from app.exeptions.server import exceptions as server_exception
from app.exeptions.server import handlers as server_handlers


def setup_exeption_handler(app: FastAPI):
    app.add_exception_handler(
        exc_class_or_status_code=client_exception.TokenException,
        handler=client_handlers.token_exception_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=client_exception.AuthException,
        handler=client_handlers.auth_exception_handler
    )
    app.add_exception_handler(
        exc_class_or_status_code=RequestValidationError,
        handler=client_handlers.request_exception_handler
    )
    app.add_exception_handler(
        exc_class_or_status_code=server_exception.ServerError,
        handler=server_handlers.server_error_handler
    )
