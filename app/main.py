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

# TODO - create product models in database
# TODO - create product schemes
# TODO - create caching requests
# TODO - add HATEOAS
# TODO - write tests
# TODO - create handler error
# TODO - add black
# TODO - add order_by for user_list response
# TODO - write error handler in endpoints
