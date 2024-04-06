FROM python:3.11

WORKDIR /spb_base

RUN pip install poetry

COPY pyproject.toml poetry.lock* /spb_base/

COPY .env ./
COPY src src

RUN poetry install --no-interaction --no-ansi


CMD ["poetry", "run", "uvicorn", "spb_base.main:main", "--factory", "--reload", "--host", "0.0.0.0", "--port", "8081"]