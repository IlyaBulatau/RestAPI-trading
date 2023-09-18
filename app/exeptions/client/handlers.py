from fastapi import Request
from fastapi.responses import JSONResponse

from app.exeptions.client.exeptions import TokenException


async def token_exception_handler(request: Request, exc: TokenException):
    return JSONResponse(content=exc.detail, status_code=exc.status_code)
