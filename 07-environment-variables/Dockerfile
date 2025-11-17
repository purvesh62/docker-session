FROM python:3.9-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy project files
COPY pyproject.toml /app/

# Install dependencies using uv
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy application code
COPY app.py /app/

# Set default environment variables (can be overridden)
ENV APP_NAME="Environment Demo App" \
    APP_VERSION="1.0.0" \
    ENVIRONMENT="production" \
    DEBUG="false" \
    MAX_CONNECTIONS="100"

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
