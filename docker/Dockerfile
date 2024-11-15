FROM python:3.12.7-alpine AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY  ./requirements/ /app/requirements

RUN apk add --no-cache gcc python3-dev musl-dev linux-headers

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /app/requirements/base.txt

COPY . /app
RUN chmod -R 777 /app

FROM base AS test

RUN pip install -r /app/requirements/test.txt

CMD ["python", "manage.py", "test"]

FROM base AS production
WORKDIR /app

ENV WORKERS=4
ENV MAX_REQUESTS=1000
ENV MAX_REQUESTS_JITTER=50
ENV BIND="0.0.0.0:8000"
ENV DJANGO_SETTINGS_MODULE=address.settings.production
RUN pip install --no-cache-dir -r /app/requirements/production.txt
COPY ./docker/entrypoints/production.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]