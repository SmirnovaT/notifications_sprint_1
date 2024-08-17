FROM python:3.11-slim

EXPOSE 8000

WORKDIR /opt/app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE 0
ENV POETRY_NO_INTERACTION 1


RUN  pip install --upgrade pip && pip install poetry==1.8.3

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

ENTRYPOINT python ./src/main.py