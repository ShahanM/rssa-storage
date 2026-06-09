FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client libpq-dev gcc curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY . .

RUN uv pip install --system -e .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
