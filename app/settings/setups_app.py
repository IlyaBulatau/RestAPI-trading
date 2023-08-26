from fastapi import FastAPI

from app.auth.handlers import router as auth_router


def setup_router(app: FastAPI) -> None:
    app.include_router(auth_router)    


def setup_app(app: FastAPI) -> None:
    setup_router(app)