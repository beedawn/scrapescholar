import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access an environment variable
api_key = os.getenv('SCIENCEDIRECT_APIKEY')
#keyword for search
keyword = "cybersecurity"
# triggers for science direct endpoint
def request_api():
    #request data from science direct
    response = requests.get(f"https://api.elsevier.com/content/search/sciencedirect?query={keyword}&apiKey={api_key}")
    #get json data
    data = response.json()
    #get search-results object
    search_results= data.get('search-results', {})
    #get entries list
    entries = search_results.get('entry',[])
    #return entries to sciencedirect endpoint response
    return entries
