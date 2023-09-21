from fastapi import FastAPI

from app.settings.setups_app import setup_app


app = FastAPI(
    title="REST Store",
    description="Store Servise with REST architecture",
    version="0.1.0",
    contact={
        "name": "Ilya",
        "url": "https://t.me/ilbltv",
        "email": "ilyabulatau@gmail.com",
    },
)

setup_app(app)

# TODO - write tests
# TODO - add celery for smtp logging
# TODO - create wallets and ability buy products
# TODO - create rate limiting
# TODO - return headers in responses
