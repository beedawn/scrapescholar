# Use an official Python image as the base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the entire backend folder to the Docker image
COPY ../../backend /app/backend

# Copy the init_db script to the Docker image
COPY docker/postgres/init_db.sh /app/init_db.sh

# Install dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Make init_db.sh executable
RUN chmod +x /app/init_db.sh

# Entrypoint to initialize the database
ENTRYPOINT ["/app/init_db.sh"]
