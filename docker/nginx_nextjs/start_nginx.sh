#!/bin/sh


# Substitute environment variables in the NGINX template
envsubst '\$NGINX_HOST \$NGINX_PORT' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Print the generated configuration (for debugging purposes)
echo "Generated NGINX config:"
cat /etc/nginx/conf.d/default.conf

# Start NGINX in the foreground (daemon off)
nginx -g 'daemon off;'
