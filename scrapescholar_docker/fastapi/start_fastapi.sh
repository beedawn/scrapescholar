#!/bin/sh

if [ -f /etc/nginx/ssl/live/${HOST_IP}/fullchain.pem ] && \
   [ -f /etc/nginx/ssl/live/${HOST_IP}/privkey.pem ] && \
   { [ "$ENVIRONMENT" = "prod" ] || [ "$ENVIRONMENT" = "production" ] || \
     [ "$ENVIRONMENT" = "PROD" ] || [ "$ENVIRONMENT" = "PRODUCTION" ]; }; then 
    echo "Serving SSL FastAPI"
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile /etc/nginx/ssl/live/${HOST_IP}/privkey.pem --ssl-certfile /etc/nginx/ssl/live/${HOST_IP}/fullchain.pem
else
    echo "Serving Port 8000 FastAPI"
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
fi