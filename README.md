# ScrapeScholar

This is a web application to assist with systematic literature reviews. It utilizes Next.js, FastAPI, and Postgres.

This application has also been dockerized. Since it is dockerized, all you will need to do is set up the proper environment variables and run the docker compose file in scrapescholar_docker/.

To build the proper environment variable files, you can navigate to install/ and select the windows or linux directories. The linux scripts also work on MacOS. Once in one of these directories, run the install file for your OS (Linux/Mac: install.sh, Windows: install.bat). For Linux/mac you will also need to run:
```
chmod +x install.sh
```
Before executiing the install script. The install script will also create self signed certs, these are primarily for local deployment. If you intend to serve this application publically, then enter the domain you intend to host the site on when prompted during the install script.

You will then need to clone this repo onto the machine that will host the website and run the install/linux/cert_install/ssl_generation_run_from_virtualmachine.sh script from that machine. Please see the readme in the cert_install/ directory for more details.

## For development purposes you can review the below section on how to run pieces of the application.

To run the front end navigate to client/scrape_scholar_client and run 

```bash
npm install
npm run dev
```
To run the front end tests run
```bash
npm test
```

To run the backend navigate to backend/ and create a virtual environment with:

Linux Bash
```bash

python -m venv .venv
```

Windows Powershell
```powershell
c:\>Python35\python -m venv c:\path\to\myenv
```


Then activate the virtual environment:

Linux Bash
```bash

source .venv/bin/activate
```

Windows Powershell
```powershell
.venv\Scripts\Activate.ps1
```

Then run this script to install the requirements
```bash
pip install -r requirements.txt
```


Then to launch the backend run
```bash
fastapi run
```

To run the backend tests run
```bash
python -m pytest tests/
```


Tests with coverage
```bash
coverage run -m pytest tests --verbose && coverage report -m
```

next js with coverage
```bash
npm run test:unit -- --coverage
```


To create test database please do the following 
```
CREATE DATABASE scrapescholartestdb;

CREATE USER student WITH PASSWORD 'student';

GRANT ALL PRIVILEGES ON DATABASE scrapescholartestdb TO student;

python -m app.init_db
```



login curl:
curl -X 'POST' \
  'http://localhost:8000/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=admin&password=admin1234&scope=&client_id=string&client_secret=string'
