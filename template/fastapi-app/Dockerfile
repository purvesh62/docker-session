# Base image
FROM python:3.14.0-slim

# Working directory
WORKDIR /app

# Copy project files
COPY requirements.txt requirements.txt

# Install dependencies using pip
RUN pip install --no-cache -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]