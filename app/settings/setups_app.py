from fastapi import FastAPI

from app.auth.handlers import router as auth_router
from app.api.handlers.users import router as user_router
from app.api.handlers.products import router as product_router
from app.exeptions import setup_exeption_handler


def setup_router(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(product_router)


def setup_app(app: FastAPI) -> None:
    setup_router(app)
    setup_exeption_handler(app)
