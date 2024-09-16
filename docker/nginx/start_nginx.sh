#!/bin/sh

#chomd +x start_nginx.sh before running this container
envsubst '${SERVER_NAME}' < /etc/nginx/conf.d/templates/app.conf.template > /etc/nginx/conf.d/app.conf

exec nginx -g 'daemon off;'