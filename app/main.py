from fastapi import FastAPI

from app.settings.setups_app import setup_app
from app.servise.bg_tasks.tasks import send_to_email_log


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
send_to_email_log.delay("SERVER APP")
setup_app(app)

# TODO - create wallets and ability buy products
# TODO - create rate limiting
# TODO - return headers in responses
