FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --without dev

ADD ./darwin /app/darwin

EXPOSE $PORT

CMD uvicorn darwin.web.app:app --host 0.0.0.0 --port $PORT
