# Multi-stage build for optimized image size

# Stage 1: Builder stage
FROM python:3.14.0-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml /app/

# Install dependencies to a specific directory
RUN uv pip install --system --no-cache -r pyproject.toml

# Stage 2: Runtime stage
FROM python:3.14.0-slim

# Create non-root user for security
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Copy application code
COPY app.py /app/

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
