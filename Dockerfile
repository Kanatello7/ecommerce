FROM python:3.12-slim

WORKDIR /app 

RUN apt-get update -y && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:${PATH}"

COPY poetry.lock pyproject.toml . 

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root

COPY . . 


EXPOSE 8000 
CMD ["./entrypoint.sh"]