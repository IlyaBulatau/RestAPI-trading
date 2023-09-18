from fastapi import Request
from fastapi.responses import JSONResponse

from app.exeptions.client.exeptions import TokenException, AuthException


async def token_exception_handler(request: Request, exc: TokenException):
    return JSONResponse(content=exc.detail, status_code=exc.status_code)


async def auth_exception_handler(request: Request, exc:AuthException):
    print(request)
    return JSONResponse(content=exc.detail, status_code=exc.status_code)