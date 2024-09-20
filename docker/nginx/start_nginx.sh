#!/bin/sh

#chomd +x start_nginx.sh before running this script

if [ -f /etc/nginx/ssl/live/${SERVER_NAME}/fullchain.pem ] && [ -f /etc/nginx/ssl/live/${SERVER_NAME}/privkey.pem ]; then
    echo "SSL certificates found. Using SSL nginx template."

    envsubst '${SERVER_NAME}' < /etc/nginx/templates/app-ssl.conf.template > /etc/nginx/conf.d/app.conf
else
    echo "No SSL certificates found, using basic template only port 80"

    envsubst '${SERVER_NAME}' < /etc/nginx/templates/app.conf.template > /etc/nginx/conf.d/app.conf
fi
#start nginx
exec nginx -g 'daemon off;'