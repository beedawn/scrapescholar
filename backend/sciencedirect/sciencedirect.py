import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access an environment variable
api_key = os.getenv('SCIENCEDIRECT_APIKEY')
keyword = "cybersecurity"
def request_api():
    response = requests.get(f"https://api.elsevier.com/content/search/sciencedirect?query={keyword}&apiKey={api_key}")
    data = response.json()
    search_results= data.get('search-results', {})
    entries = search_results.get('entry',[])
    return entries
