FROM python:3.9-slim

WORKDIR /app

# Install dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agents/ agents/
COPY scripts/ scripts/

ENV PYTHONPATH="/app"

CMD ["python", "scripts/python/cli.py"]
