# ScrapeScholar

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
backend % coverage run --source=app -m pytest tests --verbose && coverage report -m
```

next js with coverage
```bash
npm run tests:unit -- --coverage
```