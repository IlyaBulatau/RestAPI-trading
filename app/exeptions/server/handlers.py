from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import ValidationException

from app.exeptions.server.shemes import ServerExceptionSchemes


async def server_error_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=500,
        content=ServerExceptionSchemes(message="Ops, temporary problems on the server").model_dump()
        )