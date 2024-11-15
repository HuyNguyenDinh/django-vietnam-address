#!/bin/sh

gunicorn address.asgi:application --workers ${WORKERS} --max-requests ${MAX_REQUESTS} --max-requests-jitter ${MAX_REQUESTS_JITTER} -k uvicorn_worker.UvicornWorker --bind ${BIND} --access-logfile="-"