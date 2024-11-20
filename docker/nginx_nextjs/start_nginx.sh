# #!/bin/sh



# envsubst '\$NGINX_HOST \$NGINX_PORT' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf


# echo "Generated NGINX config:"
# cat /etc/nginx/conf.d/nginx.conf


# echo "nginx conf"
# cat /etc/nginx/conf.d/nginx.conf
# # Start NGINX in the foreground (daemon off)
# nginx -g 'daemon off;'





#!/bin/sh

#chomd +x start_nginx.sh before running this script

if [ -f /etc/nginx/ssl/live/${SERVER_NAME}/fullchain.pem ] && [ -f /etc/nginx/ssl/live/${SERVER_NAME}/privkey.pem ]; then
    echo "SSL certificates found. Using SSL nginx template."

    envsubst '\$SERVER_NAME' < /etc/nginx/templates/app-ssl.conf.template > /etc/nginx/conf.d/default.conf
else
    echo "No SSL certificates found, using basic template only port 80"

    envsubst '\$NGINX_HOST \$NGINX_PORT' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf
fi
#start nginx
exec nginx -g 'daemon off;'