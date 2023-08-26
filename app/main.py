from fastapi import FastAPI

from app.settings.setups_app import setup_app


app = FastAPI()

setup_app(app)