FROM python:3.11-buster
RUN pip install poetry==1.4.2
WORKDIR /app
COPY pyproject.toml poetry.lock README.md ./
COPY currency-exchange-processor ./currency-exchange-processor

RUN poetry install --without dev

ENTRYPOINT ["poetry", "run", "python", "-m", "currency-exchange-processor.etl_scripts.job_runner.start"]
