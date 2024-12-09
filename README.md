# ScrapeScholar


1 Installation Instructions  

1.1 Product Overview  

ScrapeScholar uses a variety of open-source technologies in orchestration to provide its functionality. These technologies include Next.js, Fast API, PostgreSQL, and SQL Alchemy.  

1.2 GitHub Repository 

https://github.com/beedawn/scrapescholar 

1.3 List of tools, frameworks, and services to run the system.  

The primary tool used to run the system is the docker container platform. This tool facilitates programmatic deployment of various technologies used within the application. The docker build consists of a PostgreSQL database, a Fast API application, and a Next.js application. The PostgreSQL database handles data storage and persistence between sessions. The Fast API application handles business logic and performs transactions on the PostgreSQL database using the SQL Alchemy Object Relational Mapper. The Next.js application serves as the user interface to enhance the user experience and allow them to perform HTTPS requests to the Fast API to perform various transactions on the database and the business logic. 

1.4 Instructions to download and install each tool  

1.4.1 Docker 

Docker is available via the Docker website, https://www.docker.com/ and they provide a Docker Desktop client which provides an intuitive user interface to manage docker containers. This application is available for all major operating systems and computing architectures. Docker Desktop is designed for development purposes, and in production a Linux system should be used to serve the application via the Docker CLI. 

Docker largely handles the deployment of the application, as it builds the docker containers for each piece of the application with docker compose. For development purposes, the other components can be downloaded individually, and the next following sections elaborate on how to deploy each component individually. If you deploy the application with docker, you do not need to follow the below sections. 

1.4.2 Fast API 

Fast API is a python web framework for building APIs. To use this framework, you will need to download Python if it is not already installed on your OS. To check if python is installed you can open a terminal on your machine (command prompt, PowerShell, bash, etc.) you can type: 

python --version 

 
This command should show the python version, if it is installed. If it shows Python 2.x.x you may need to run: 

python3 --version 

 

Our application uses Python 3. Specifically, we have used Python 3.11.7 for developing this application. If it is not installed it can be downloaded from the Python website: https://www.python.org/downloads/  

Once installed, you can run the above commands to determine if Python3 was the version installed. After installation, it is recommended to create a python virtual environment, to isolate the packages and dependencies from the local system. A virtual environment can be instantiated by running the command: 

python –m venv /path/to/environment 

 

The environment will then need to be activated, for up-to-date specific instructions on how to activate the virtual environment you can visit the documentation here: 
https://docs.python.org/3/library/venv.html  

Once activated, all the dependencies for our project can be installed using the requirements.txt file in the /backend directory within the repository, with the following command: 

pip install –r requirements.txt 

 

This will download all the dependencies needed to build the application. The Fast API portion of the application can then be initialized by navigating to the /backend directory and running the command: 

fastapi run 

However, you will need to install PostgreSQL before running this command so please review section 1.4.3 for further instruction on how to initialize the database. 

1.4.3 PostgreSQL 

To install PostgreSQL, you should navigate to their webpage: https://www.postgresql.org/download/  
Once on this page you can find instructions for your operating system. Please note before proceeding you should have Python installed with all the associated dependencies in section 1.4.2. Once PostgreSQL is installed you should be able to access PostgreSQL by entering the command: 

Mac/Linux 

psql –U postgres 

Windows (PostgreSQL 17) 

C:\Program Files\PostgreSQL\17\scripts\runpsql.bat 

 

Once you are in the PSQL prompt you can run the following commands 

CREATE DATABASE scrapescholartestdb; 

CREATE USER student WITH PASSWORD 'student'; 

GRANT ALL PRIVILEGES ON DATABASE scrapescholartestdb TO student; 

 

Then in a separate command prompt, from the backend directory run: 

python -m app.init_db 

 

This Python script automates the creation of all the needed tables and relations within the database and sets up the test user and test password needed as an initial account to sign in and grant access to other users. 

1.4.4 Next.js 

To install the Next.js portion, you will first need to download Node.js. The latest instructions can be found here: https://nodejs.org/en/download/package-manager Our project uses node v20.10.0. After following those instructions, you should be able to navigate to the /client/scrapescholar_client directory and run: 

npm install 

 

To install all the associated dependencies associated with our project. Once this is completed, you can run: 

npm run dev 

 
To build the Next.js development build and you can then access the application at http://localhost:3000 in a web browser. Please note that ScrapeScholar has been primarily tested with chromium-based browsers such as Google Chrome, and Microsoft Edge. We cannot guarantee compatibility with non-chromium-based browsers such as Firefox or Safari. 

1.5 Instructions for the environment configuration  

1.5.1 Environment Variables 

The project requires three .env files, one in the client/scrapescholar_client directory (Next.js), one in the backend/ directory (Fast API), and one in the scrapescholar_docker/ directory (Docker). 

The installation scripts located in the repositories’ /install directory automate the process of building the .env files for each respective directory. These install files should be run as root, or administrator in Microsoft Windows. Each file and the environment required variables are discussed in depth in the following sections. 

1.5.1.1 Next.js Environment Variables 

The environment variables discussed here refer to the environment variables stored in the ./client/scrapescholar_client/.env file of the project. This file requires two environment variables: 

NEXT_PUBLIC_HOST_IP=localhost 
NEXT_PUBLIC_ENVIRONMENT=PRODUCTION 

 

The NEXT_PUBLIC_HOST_IP environment variable sets the domain for the API requests made by the app/api/apiCalls.tsx file. For most deployments, this should be set to localhost. Especially when using our docker compose build to compile the application. However, it may be necessary to change this for advanced configurations that differ from our docker build, such as a publicly facing website, or instances where the Fast API application is hosted from a different machine than the Next.js application. 

The NEXT_PUBLIC_ENVIRONMENT environment variable should be set to production when SSL certificates are configured, and when it is set to production will set the requests in the app/api/apiCalls.tsx file to use https to make requests to the backend portion of the application. When the NEXT_PUBLIC_ENVIRONMENT is not set to production or does not exist then Next.js will serve requests to Fast API via unsecure http requests. 

It is also important to note that Next.js requires the NEXT_PUBLIC portion to be prepended to all environment variables, or it will not read them. An example of this environment file with generic values can be found in the example.env file of the /client/scrapescholar_client directory in the repository. 

1.5.1.2 Fast API Environment Variables 

The environment variables discussed here pertain to the env file found at /backend/.env of the project. 

This file has 17 environment variables, with one optional one. Below is a list of each environment variable. The optional environment variable is SCOPUS_INSTTOKEN. 

SCIENCEDIRECT_APIKEY=api_key 

SCOPUS_APIKEY=api_key 

SCOPUS_INSTTOKEN=institutional_api_key # optional 

POSTGRES_USER=postgres_user 

POSTGRES_PASSWORD=postgres_pass 

POSTGRES_DB=db_name 

POSTGRES_SERVER=localhost or 0.0.0.0 

POSTGRES_PORT=5432 

SECRET_KEY=secret_key 

ENCRYPTION_KEY=encryption_key 

TEST_USER=username 

TEST_PASSWORD=password 

THESAURUS_APIKEY=merriamwebster_thesaurus_api_key 

HOST_IP=localhost or 0.0.0.0 

AZURE_CLIENT_SECRET=azure_client_secret 

AZURE_CLIENT_ID=azure_client_id 

AZURE_TENANT_ID=azure_tenant_id 

 
The first variable listed is the SCIENCEDIRECT_APIKEY this is the Science Direct API Key provided by Elsevier, this key can be acquired at the following link https://dev.elsevier.com/ and can be tested it with their Interactive API tool, listed under the “Start Coding” link in the top right corner of the page. The second variable SCOPUS_APIKEY, is also an API key provided by Elsevier, and can be acquired at the previously listed link. In theory, you should be able to use the same API key for both fields. If you experience any difficulties or are unable to use the “Start Coding” tool mentioned above, it is best to contact Elsevier support. They can be contacted by visiting https://dev.elsevier.com/ and clicking the “Contact Us” link. The third environment variable is SCOPUS_INSTTOKEN, this is another Elsevier API key. To acquire this key, you must contact Elsevier support and request an Institutional API key, and this key is optional. Configuring the SCOPUS_INSTTOKEN will allow the application to provide abstracts alongside the other relevant article information. 

The next environment variable is POSTGRES_USER. This is the username which the application will use to access the database. Next, there is POSTGRES_PASS which is the password the POSTGRES_USER will use to access the PostgreSQL Database. After that, there is POSTGRES_PORT, which is set to the PostgreSQL default port of 5432. The next value is SECRET_KEY, this is used to encrypt the login session information. In the following line we have ENCRYPTION_KEY, this is used to encrypt the data within the database. After that we have TEST_USER, and TEST_PASS. These are the username and password for the initial available user for the application. This account can be used to grant initial access to other users. 

Next, we have the THESAURUS_APIKEY, this is a Merriam Webster Collegiate Thesaurus API Key which can be acquired here: https://dictionaryapi.com/products/api-collegiate-thesaurus The variable after that is HOST_IP, this is the IP/domain name of the hosting domain. For local hosting, you can use localhost. This is primarily used to set the CORS policy for Fast API and set the domain for the redirect URL for Azure OAuth. 

Lastly, we have three Azure associated variables. AZURE_CLIENT_ID is the Azure Entra Client ID. AZURE_TENANT_ID is the Azure Entra Tenant ID. The AZURE_CLIENT_SECRET is the Azure Entra client secret. Obtaining these credentials will be discussed in section 1.5.1.4. 

1.5.1.3 Docker Environment Variables 

The environment variables discussed here pertain to the .env file found at /scrapescholar_docker/.env of the project, 

This file has 17 environment variables, with one optional one. Below is a list of each environment variable. 

SCIENCEDIRECT_APIKEY=api_key 

SCOPUS_APIKEY=api_key 

SCOPUS_INSTTOKEN=institutional_api_key #Optional 

POSTGRES_USER=postgres_user 

POSTGRES_PASSWORD=postgres_pass 

POSTGRES_DB=db_name 

POSTGRES_SERVER=localhost or 0.0.0.0 

POSTGRES_PORT=5432 

DATABSE_URL=postgresql://username:password@db:5432/db_name 

SECRET_KEY=secret_key 

ENCRYPTION_KEY=encryption_key 

TEST_USER=username 

TEST_PASSWORD=password 

AZURE_CLIENT_SECRET=azure_client_secret 

AZURE_CLIENT_ID=azure_client_id 

AZURE_TENANT_ID=azure_tenant_id 

THESAURUS_APIKEY=merriamwebster_thesaurus_api_key 

HOST_IP=localhost or 0.0.0.0 

ENVIRONMENT=PRODUCTION 

 
These environment variables are largely the same as the ones discussed in section 1.5.1.2, so they will not be elaborated on again here. For information regarding each environment variable please see section 1.5.1.2 

1.5.1.4 Azure 

To utilize the “Sign in with Azure AD” button at the login screen of the application, an Azure Client ID, Azure Tenant ID and Azure Client Secret must be obtained from the Azure Entra portal. The following link will provide these to you, if you have access to your institution’s Azure portal and have the ScrapeScholar provisioned an application assignment within Azure. 
 
https://aad.portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/~/Overview/appId/53d63a26-224c-4934-ba66-a31a2a06870e 

After clicking this link, you will be presented in a view similar to Figure 2. This page displays the Azure Client ID and Azure Tenant ID. 

 
Figure 2: Screenshot of Azure Entra page showing Client and Tenant ID. 

Additional configurations are required within Azure, redirect URI’s must be configured, which are available under the Manage > Authentication blade in azure, shown in Figure 3. You will need to at least configure https://localhost:8000/azure/auth/callback as a URI in this section. For development purposes you can also configure http://localhost:8000/azure/auth/callback which is the same URL just over http instead of https. 

 

Figure 3: Screenshot of Azure Manage > Authentication blade 

Finally, you will need to configure a Client Secret, this allows ScrapeScholar and Azure to authenticate with one another. This can be configured by going to the Manage > Certificates & secrets blade within Azure, shown in Figure 4. The environment variable accepts the “Value” field, which is exposed only when you create a secret. 

Figure 4: Screenshot of Azure Manage > Certificates & secrets blade  

1.6 Certificates 

To facilitate HTTPS, certificates must be configured. If you run the installation script in /install/linux/install.sh or /install/windows/install.bat and enter “localhost” for the “Enter IP/domain the application will be served from:” prompt then self-signed certificates will be generated by the script and saved to: /scrapescholar/scrapescholar_docker/nginx/certbot/conf/live/localhost  

It will save two files, fullchain.pem and privkey.pem. These file names align with how the Let’s Encrypt certbot creates certificates.  

To generate free SSL certificates for a publicly facing domain we have implemented Let’s Encrypt. Let’s Encrypt can be used to generate certificates if the application is served on a publicly accessible IP/domain, as certbot needs to be able to ping where the application is hosted to generate the certificates. To acquire certificates from Let’s encrypt you will need to copy the ScrapeScholar repository to the machine, then navigate to the /scrapescholar/scrapescholar_docker/nginx directory. Then open the docker-compose.yml file in this directory and change the domain name on line 19 to your domain name or IP. Then run the following from that directory: 

docker compose up –d 

chmod +x ssl_generation_run_from_virtualmachine.sh 

./ssl_generation_run_from_virtualmachine.sh 

Then run  

docker ps 

Take a note of the container ID and restart the container with the command: 

docker restart <container_id> 

The application should now have a certbot certificate installed, you can check that files exist in scrapescholar_docker/nginx/certbot/conf/live/{domain_name}/ 

Then you can run the docker compose file from /scrapescholar_docker directory with the following command: 

docker compose –f docker-compose-scrapescholar up --build 

1.7 Video Demonstration 

Here is a video of the installation process completed on the big data machine: 
scrapescholar_install.mp4 
