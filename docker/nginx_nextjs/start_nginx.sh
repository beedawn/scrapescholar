#!/bin/sh



envsubst '\$NGINX_HOST \$NGINX_PORT' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf


echo "Generated NGINX config:"
cat /etc/nginx/conf.d/nginx.conf


echo "nginx conf"
cat /etc/nginx/conf.d/nginx.conf
# Start NGINX in the foreground (daemon off)
nginx -g 'daemon off;'
