#!/bin/sh

#chomd +x start_nginx.sh before running this script

if [ -f /etc/nginx/ssl/live/${NGINX_HOST}/fullchain.pem ] && \
   [ -f /etc/nginx/ssl/live/${NGINX_HOST}/privkey.pem ] && \
   { [ "$ENVIRONMENT" = "prod" ] || [ "$ENVIRONMENT" = "production" ] || \
     [ "$ENVIRONMENT" = "PROD" ] || [ "$ENVIRONMENT" = "PRODUCTION" ]; }; then 
     echo "SSL certificates found. Using SSL nginx template."

    envsubst '\$NGINX_HOST' < /etc/nginx/templates/app-ssl.conf.template > /etc/nginx/conf.d/default.conf
else
    echo "No SSL certificates found, using basic template only port 80"

    envsubst '\$NGINX_HOST' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf
fi
#start nginx
exec nginx -g 'daemon off;'