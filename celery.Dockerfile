FROM python:3.10.6-buster

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /celery

RUN pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false

COPY . .

COPY .env .

RUN poetry install --no-interaction --no-ansi

COPY celery-entrypoint.sh .

RUN chmod 777 celery-entrypoint.sh

ENTRYPOINT [ "./celery-entrypoint.sh" ]

