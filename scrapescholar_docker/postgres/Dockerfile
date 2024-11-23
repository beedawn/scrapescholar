# Use an official Python image as the base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the entire backend folder to the Docker image
COPY ../../backend /app/backend

# Copy the .env file
COPY scrapescholar_docker/.env /app/.env

# Copy the init_db script to the Docker image
COPY scrapescholar_docker/postgres/init_db.sh /app/init_db.sh

# Install PostgreSQL client
RUN apt-get update -o Acquire::http::Timeout=600 && apt-get install -y postgresql-client iputils-ping

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt --timeout 120

# Make scripts executable
RUN chmod +x /app/init_db.sh

# Entrypoint to initialize the database
ENTRYPOINT ["/app/init_db.sh"]