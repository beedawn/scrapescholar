#!/bin/bash

# Load environment variables
source /app/.env

# Wait for the PostgreSQL server to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h "$POSTGRES_SERVER" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  sleep 2
done

echo "PostgreSQL is ready. Running database initialization..."

# Run the initialization script
python /app/backend/app/init_db.py

echo "Database initialized successfully."