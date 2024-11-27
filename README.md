# ScrapeScholar

To run the front end navigate to client/scrapescholar_client and run 

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

CREATE DATABASE scrapescholartestdb;

CREATE USER student WITH PASSWORD 'student';

GRANT ALL PRIVILEGES ON DATABASE scrapescholartestdb TO student;

python -m app.init_db

create user curl
curl -X 'POST' \
  'http://localhost:8000/users/create' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "admin",
  "email": "admin@example.com",
  "password": "admin1234",
  "role_id": 1
}'


login curl:
curl -X 'POST' \
  'http://localhost:8000/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=admin&password=admin1234&scope=&client_id=string&client_secret=string'
