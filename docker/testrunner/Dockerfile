FROM python:3.11

WORKDIR /spb_base

RUN pip install poetry

COPY pyproject.toml poetry.lock* /spb_base/

COPY test.env pytest.ini ./
COPY src src
COPY tests tests

RUN poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "pytest", "tests"]
