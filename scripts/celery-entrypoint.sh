#!/bin/sh

celery -A app.servise.bg_tasks.tasks:celery worker