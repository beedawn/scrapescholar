#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
    echo "PostgreSQL is unavailable - retrying"
    sleep 2
done

echo "PostgreSQL is ready. Running database initialization..."

# Export PYTHONPATH
export PYTHONPATH=/app/backend

# Run the database initialization script
python /app/backend/app/init_db.py

echo "Database initialized successfully."
