# Use official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ /app/src/
COPY app/ /app/app/
COPY configs/ /app/configs/
COPY models/ /app/models/
COPY data/raw/ /app/data/raw/

# Create non-root user for security
RUN adduser --disabled-password --gecos "" apiuser && chown -R apiuser:apiuser /app
USER apiuser

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
