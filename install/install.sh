#!/bin/bash

filepath="testfile"

next_js_env="next_js_file_path"


echo 'Welcome to the scripted setup'
echo 'Setting up backend env file'

echo  "Enter Science Direct API Key, the key can be obtained here: https://dev.elsevier.com/ :" 
read sciencedirect_apikey
echo -e "SCIENCEDIRECT_APIKEY=${sciencedirect_apikey}" > "$filepath"

echo "Enter Scopus API Key, the key can be found at https://dev.elsevier.com/ :"
read scopus_apikey
echo -e "SCOPUS_APIKEY=${scopus_apikey}" >> "$filepath"


echo "Enter postgres username:"
read postgres_user
echo -e "POSTGRES_USER=${postgres_user}">> "$filepath"


echo "Enter postgres password:"
read postgres_pass
echo -e "POSTGRES_PASSWORD=${postgres_pass}">> "$filepath"

echo "Enter postgres db name:"
read postgres_db
echo -e "POSTGRES_DB=${postgres_db}">> "$filepath"

echo "Enter postgres server IP:"
read postgres_ip
echo -e "POSTGRES_SERVER=${postgres_ip}">> "$filepath"



echo "Enter postgres server Port:"
read postgres_port
echo -e "POSTGRES_SERVER=${postgres_port}">> "$filepath"


echo "Enter Secret Key:"
read secret_key
echo -e "SECRET_KEY=${secret_key}">> "$filepath"


echo "Enter Encryption Key:"
read encryption_key
echo -e "ENCRYPTION_KEY=${encryption_key}">> "$filepath"

echo "Enter Merriam Webster Collegiate Thesaurus API Key, can be found here https://dictionaryapi.com/products/api-collegiate-thesaurus :"
read thesaurus_apikey
echo -e "THESAURUS_APIKEY=${thesaurus_apikey}" >> "$filepath"

echo "Enter initial admin user"
read admin_user
echo -e "TEST_USER=${admin_user}" >> "$filepath"

echo "Enter initial admin password"
read admin_pass
echo -e "TEST_PASSWORD=${admin_pass}" >> "$filepath"

echo "Enter IP/domain the application will be served from:"
read host_ip
echo -e "HOST_IP=${host_ip}" >> "$filepath"
echo -e "NEXT_PUBLIC_HOST_IP=${host_ip}">> "$next_js_env"

