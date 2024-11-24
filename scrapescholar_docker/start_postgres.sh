#!/bin/bash
docker compose -f docker-compose-postgres.yml --env-file .env up --build