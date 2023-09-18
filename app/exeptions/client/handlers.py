from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.exeptions.client.exeptions import TokenException, AuthException
from app.exeptions.client.shemas import RequestValidationScheme


async def token_exception_handler(request: Request, exc: TokenException):
    return JSONResponse(content=exc.detail, status_code=exc.status_code)


async def auth_exception_handler(request: Request, exc:AuthException):
    return JSONResponse(content=exc.detail, status_code=exc.status_code)


async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=RequestValidationScheme(
            code=422,
            message="Please, enter all required fields"
    ).model_dump())