#!/bin/bash

# Set filenames
KEY_FILE="localhost.key"
CSR_FILE="localhost.csr"
CRT_FILE="localhost.crt"
PEM_FILE="localhost.pem"

echo "Generating private key..."
openssl genpkey -algorithm RSA -out $KEY_FILE -aes256
if [[ $? -ne 0 ]]; then
  echo "Error generating private key."
  exit 1
fi


echo "Generating CSR..."
openssl req -new -key $KEY_FILE -out $CSR_FILE -subj "/C=US/ST=California/L=Los Angeles/O=MyCompany/CN=localhost"
if [[ $? -ne 0 ]]; then
  echo "Error generating CSR."
  exit 1
fi


echo "Generating self-signed certificate..."
openssl x509 -req -in $CSR_FILE -signkey $KEY_FILE -out $CRT_FILE -days 365
if [[ $? -ne 0 ]]; then
  echo "Error generating certificate."
  exit 1
fi


echo "Combining certificate and private key into a PEM file..."
cat $KEY_FILE $CRT_FILE > $PEM_FILE


echo "Self-signed certificate and private key generated successfully!"
echo "Files generated:"
echo "  Private Key: $KEY_FILE"
echo "  Certificate: $CRT_FILE"
echo "  Combined PEM: $PEM_FILE"