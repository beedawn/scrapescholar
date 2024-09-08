# ScrapeScholar

To run the front end navigate to client/scrape_scholar_client and run 

```bash
npm install
npm run dev
```


To run the backend navigate to backend/ and create a virtual environment with:

Linux
```bash

python -m venv .venv
```

Windows
```powershell
c:\>Python35\python -m venv c:\path\to\myenv
```


Then activate the virtual environment
Linux

```bash

source .venv/bin/activate
```

Windows
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
