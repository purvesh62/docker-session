FROM python:3.9-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy project files
COPY pyproject.toml /app/

# Install dependencies using uv
RUN uv pip install --system --no-cache -r pyproject.toml

# Note: In development with bind mount, we won't COPY app.py
# The bind mount will provide it at runtime
COPY app.py /app/

EXPOSE 8000

# Enable hot reload for development
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
