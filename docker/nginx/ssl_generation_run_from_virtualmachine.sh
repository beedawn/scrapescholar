#!/bin/bash

# run docker container with
# docker compose up -d
# then run this script with www.yourdomain.com
printf "%s" "enter domain name: "
read server_name
docker compose run --rm certbot certonly --webroot \
    --webroot-path /var/www/certbot \
    -d scrapescholar.me -d www.scrapescholar.me

if [ $? -eq 0 ]; then
    echo "Dry run successful. Proceeding to obtain the certificate."
    docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d "$server_name"
else
    echo "Dry run failed. Please check the logs for more details."
fi