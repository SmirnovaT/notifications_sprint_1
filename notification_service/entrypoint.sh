#!/usr/bin/env bash

gunicorn src.main:app --bind 0.0.0.0:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker --access-logfile - --error-logfile -