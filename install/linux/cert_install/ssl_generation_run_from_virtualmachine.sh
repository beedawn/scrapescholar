#!/bin/bash

# run docker container with
# docker compose up -d
# then run this script with yourdomain.com

if [ -z "$(docker ps -q -f name=nginx)" ]; then 
        echo "Nginx is not running, please run docker compose up -d from the nginx directory and try again."
        exit
fi 




printf "%s" "enter domain name(ie google.com, no www): "
read server_name
docker compose run --rm certbot certonly --webroot \
    --webroot-path /var/www/certbot \
    -d $server_name -d www.$server_name

if [ $? -eq 0 ]; then
    echo "Dry run successful. Proceeding to obtain the certificate."
    docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d "$server_name"
else
    echo "Dry run failed. Please check the logs for more details."
fi