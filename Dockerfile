# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies and gunicorn
# We strip '.' from requirements.txt to install external deps first (better caching)
RUN grep -v "^\.$" requirements.txt > requirements_no_local.txt && \
    pip install --no-cache-dir -r requirements_no_local.txt gunicorn

# Copy the rest of the application code into the container
COPY . .

# Install the local package
RUN pip install --no-cache-dir .

# Create a non-root user for security
RUN addgroup --system app && adduser --system --group app
USER app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using Gunicorn for production
CMD ["sh", "-c", "gunicorn api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}"]
