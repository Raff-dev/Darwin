FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD ./darwin /darwin

WORKDIR /darwin

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local

COPY ./pyproject.toml ./poetry.lock* /darwin/

RUN poetry install --without dev

EXPOSE $PORT

CMD uvicorn app:app --host 0.0.0.0 --port $PORT --reload
