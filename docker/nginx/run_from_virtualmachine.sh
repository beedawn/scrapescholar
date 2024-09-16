#!/bin/bash
printf "%s" "enter domain name: "
read server_name
docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d $server_name

if [ $? -eq 0 ]; then
    echo "Dry run successful. Proceeding to obtain the certificate."
    docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d "$server_name"
else
    echo "Dry run failed. Please check the logs for more details."
fi