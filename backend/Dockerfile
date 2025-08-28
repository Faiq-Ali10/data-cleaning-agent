# backend/Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code maintaining structure
COPY . ./backend

# Set PYTHONPATH so 'backend' module can be found
ENV PYTHONPATH=/app

# Expose port (FastAPI default)
EXPOSE 8000

# Command to run FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]