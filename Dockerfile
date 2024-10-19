FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install

EXPOSE 8000

CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"]
