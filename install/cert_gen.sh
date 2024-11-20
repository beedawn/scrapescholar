# #!/bin/bash

# # Set filenames
# KEY_FILE="localhost.key"
# CSR_FILE="localhost.csr"
# CRT_FILE="localhost.crt"
# PEM_FILE="localhost.pem"

# echo "Generating private key..."
# openssl genpkey -algorithm RSA -out $KEY_FILE -aes256
# if [[ $? -ne 0 ]]; then
#   echo "Error generating private key."
#   exit 1
# fi


# echo "Generating CSR..."
# openssl req -new -key $KEY_FILE -out $CSR_FILE -subj "/C=US/ST=California/L=Los Angeles/O=MyCompany/CN=localhost"
# if [[ $? -ne 0 ]]; then
#   echo "Error generating CSR."
#   exit 1
# fi


# echo "Generating self-signed certificate..."
# openssl x509 -req -in $CSR_FILE -signkey $KEY_FILE -out $CRT_FILE -days 365
# if [[ $? -ne 0 ]]; then
#   echo "Error generating certificate."
#   exit 1
# fi


# echo "Combining certificate and private key into a PEM file..."
# cat $KEY_FILE $CRT_FILE > $PEM_FILE


# echo "Self-signed certificate and private key generated successfully!"
# echo "Files generated:"
# echo "  Private Key: $KEY_FILE"
# echo "  Certificate: $CRT_FILE"
# echo "  Combined PEM: $PEM_FILE"


#run this before starting web app, it will generater ssl certs and place them in the certbot directory

#!/bin/bash

echo "Enter the servername, if not known put localhost:"
read server_name

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
openssl req -new -key "$KEY_FILE" -out "$SSL_DIR/localhost.csr" -subj "/C=US/ST=California/L=Los Angeles/O=MyCompany/CN=$SERVER_NAME"
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
mkdir ../docker/nginx_nextjs/certbot/conf/live
mkdir ../docker/nginx_nextjs/certbot/conf/live/$server_name
mv certs/$server_name/fullchain.pem ../docker/nginx_nextjs/certbot/conf/live/$server_name/fullchain.pem
mv certs/$server_name/privkey.pem ../docker/nginx_nextjs/certbot/conf/live/$server_name/privkey.pem
