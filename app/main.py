from fastapi import FastAPI

from app.settings.setups_app import setup_app


app = FastAPI()

setup_app(app)

# TODO - create product models in database
# TODO - create product schemes
# TODO - create caching requests
# TODO - add HATEOAS
# TODO - write tests
# TODO - create handler error
# TODO - add black

