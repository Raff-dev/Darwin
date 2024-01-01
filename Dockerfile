FROM python:3.12-slim-buster

WORKDIR /app

ADD . /app

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --without dev

EXPOSE 80

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "$PORT"]
