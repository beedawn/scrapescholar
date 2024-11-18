# Use a lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the backend folder into the Docker build context
COPY ../../backend /app

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the application port
EXPOSE 8000

# Set the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]