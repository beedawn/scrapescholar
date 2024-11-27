#!/bin/bash

filepath="../../backend/.env"
dockerfilepath="../../scrapescholar_docker/.env"

next_js_env="../../client/scrapescholar_client/.env"


echo 'Welcome to the scripted setup'
echo 'Setting up backend env file'

echo  "Enter Science Direct API Key, the key can be obtained here: https://dev.elsevier.com/ :" 
read sciencedirect_apikey
echo -e "SCIENCEDIRECT_APIKEY=${sciencedirect_apikey}" > "$filepath"
echo -e "SCIENCEDIRECT_APIKEY=${sciencedirect_apikey}" > "$dockerfilepath"

echo "Do you have a scopus institutional key obtained from scopus support? (If you don't know what this is the answer is N) Y/N?:"
read scopus_inst_response
if [[ $scopus_inst_response == "Y" || $scopus_inst_response == "y" ]]; then 
	echo "Enter Scopus institutional key" 
	read scopus_inst_key 
	echo -e "SCOPUS_INSTTOKEN=${scopus_inst_key}">>"$filepath"
	echo -e "SCOPUS_INSTTOKEN=${scopus_inst_key}">>"$dockerfilepath"
fi
	

echo "Enter Scopus API Key, the key can be found at https://dev.elsevier.com/ :"
read scopus_apikey
echo -e "SCOPUS_APIKEY=${scopus_apikey}" >> "$filepath"
echo -e "SCOPUS_APIKEY=${scopus_apikey}" >> "$dockerfilepath"


echo "Enter postgres username:"
read postgres_user
echo -e "POSTGRES_USER=${postgres_user}">> "$filepath"
echo -e "POSTGRES_USER=${postgres_user}">> "$dockerfilepath"


echo "Enter postgres password:"
read postgres_pass
echo -e "POSTGRES_PASSWORD=${postgres_pass}">> "$filepath"
echo -e "POSTGRES_PASSWORD=${postgres_pass}">> "$dockerfilepath"

echo "Enter postgres db name:"
read postgres_db
echo -e "POSTGRES_DB=${postgres_db}">> "$filepath"
echo -e "POSTGRES_DB=${postgres_db}">> "$dockerfilepath"

echo "Enter postgres server IP:"
read postgres_ip
echo -e "POSTGRES_SERVER=${postgres_ip}">> "$filepath"
echo -e "POSTGRES_SERVER=${postgres_ip}">> "$dockerfilepath"



echo "Enter postgres server Port:"
read postgres_port
echo -e "POSTGRES_PORT=${postgres_port}">> "$filepath"
echo -e "POSTGRES_PORT=${postgres_port}">> "$dockerfilepath"



#only needed for docker .env
echo -e "DATABASE_URL=postgresql://${postgres_user}:${postgres_pass}@db:${postgres_port}/${postgres_db}" >> "$dockerfilepath"
             

echo "Enter Secret Key:"
read secret_key
echo -e "SECRET_KEY=${secret_key}">> "$filepath"
echo -e "SECRET_KEY=${secret_key}">> "$dockerfilepath"


echo "Enter Encryption Key:"
read encryption_key
echo -e "ENCRYPTION_KEY=${encryption_key}">> "$filepath"
echo -e "ENCRYPTION_KEY=${encryption_key}">> "$dockerfilepath"

echo "Enter Merriam Webster Collegiate Thesaurus API Key, can be found here https://dictionaryapi.com/products/api-collegiate-thesaurus :"
read thesaurus_apikey
echo -e "THESAURUS_APIKEY=${thesaurus_apikey}" >> "$filepath"
echo -e "THESAURUS_APIKEY=${thesaurus_apikey}" >> "$dockerfilepath"

echo "Enter initial admin user"
read admin_user
echo -e "TEST_USER=${admin_user}" >> "$filepath"
echo -e "TEST_USER=${admin_user}" >> "$dockerfilepath"

echo "Enter initial admin password"
read admin_pass
echo -e "TEST_PASSWORD=${admin_pass}" >> "$filepath"
echo -e "TEST_PASSWORD=${admin_pass}" >> "$dockerfilepath"

echo "Enter IP/domain the application will be served from:"
read host_ip
echo -e "HOST_IP=${host_ip}" >> "$filepath"
echo -e "HOST_IP=${host_ip}" >> "$dockerfilepath"
echo -e "NEXT_PUBLIC_HOST_IP=${host_ip}"> "$next_js_env"


echo -e "ENVIRONMENT=PRODUCTION" >> "$filepath"
echo -e "ENVIRONMENT=PRODUCTION" >> "$dockerfilepath"
echo -e "NEXT_PUBLIC_ENVIRONMENT=PRODUCTION">> "$next_js_env"

echo "Azure Client ID (for OAUTH, if none needed leave blank):"
read azure_client_id
echo -e "AZURE_CLIENT_ID=${azure_client_id}" >> "$filepath"
echo -e "AZURE_CLIENT_ID=${azure_client_id}" >> "$dockerfilepath"

echo "Azure Tenant ID (for OAUTH, if none needed leave blank):"
read azure_tenant_id
echo -e "AZURE_TENANT_ID=${azure_tenant_id}" >> "$filepath"
echo -e "AZURE_TENANT_ID=${azure_tenant_id}" >> "$dockerfilepath"


echo "Azure Client Secret (for OAUTH, if none needed leave blank):"
read azure_client_secret
echo -e "AZURE_CLIENT_SECRET=${azure_client_secret}" >> "$filepath"
echo -e "AZURE_CLIENT_SECRET=${azure_client_secret}" >> "$dockerfilepath"



if [ "$host_ip" = "localhost" ]; then
	echo "Running cert gen"
	cd cert_install
	sh ./cert_gen.sh

else
	echo "localhost not detected as IP, if serving locally, rerun script with localhost as the IP/domain the application will be served from"
	echo "If serving publically, go to nginx directory, run docker compose up -d and then run ssl_generation_run_from_virtualmachine.sh" 
fi

