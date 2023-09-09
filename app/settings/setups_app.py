from fastapi import FastAPI

from app.auth.handlers import router as auth_router
from app.api.handlers.users import router as api_router


def setup_router(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(api_router)


def setup_app(app: FastAPI) -> None:
    setup_router(app)
