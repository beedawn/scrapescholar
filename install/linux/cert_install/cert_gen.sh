#!/bin/bash


# run this before starting web app, it will generater ssl certs and place them in the certbot directory

server_name="localhost"


# Check if SERVER_NAME is provided as an environment variable
if [ -z "$server_name" ]; then
  echo "SERVER_NAME environment variable is not set!"
  exit 1
fi

# Define the SSL directory path based on SERVER_NAME
SSL_DIR="certs/$server_name"

# Create the directory if it doesn't exist

# don't need to do this
mkdir -p "$SSL_DIR"

# Set filenames
KEY_FILE="$SSL_DIR/privkey.pem"
CRT_FILE="$SSL_DIR/fullchain.pem"

# 1. Generate private key (no encryption, for Nginx to work without password prompts)
echo "Generating private key..."
openssl genpkey -algorithm RSA -out "$KEY_FILE"
if [[ $? -ne 0 ]]; then
  echo "Error generating private key."
  exit 1
fi

# 2. Generate Certificate Signing Request (CSR)
echo "Generating CSR..."
openssl req -new -key "$KEY_FILE" -out "$SSL_DIR/localhost.csr" -subj "/C=US/ST=Pennsylvania/L=Pittsburgh/O=ScrapeScholar/CN=$SERVER_NAME"
if [[ $? -ne 0 ]]; then
  echo "Error generating CSR."
  exit 1
fi

# 3. Generate self-signed certificate
echo "Generating self-signed certificate..."
openssl x509 -req -in "$SSL_DIR/localhost.csr" -signkey "$KEY_FILE" -out "$CRT_FILE" -days 365
if [[ $? -ne 0 ]]; then
  echo "Error generating certificate."
  exit 1
fi

# Success message
echo "Self-signed certificate and private key generated successfully!"
echo "Files generated:"
echo "  Private Key: $KEY_FILE"


mkdir ../../../scrapescholar_docker/nginx/certbot/conf/live
mkdir ../../../scrapescholar_docker/nginx/certbot/conf/live/$server_name
mv certs/$server_name/fullchain.pem ../../../scrapescholar_docker/nginx/certbot/conf/live/$server_name/fullchain.pem
mv certs/$server_name/privkey.pem ../../../scrapescholar_docker/nginx/certbot/conf/live/$server_name/privkey.pem
rm -rf certs/
