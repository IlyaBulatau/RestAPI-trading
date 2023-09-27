#!/bin/sh

export $(grep -v '^#' .env | xargs)

alembic upgrade head

uvicorn app.main:app --port=$APP_PORT --host=$APP_HOST