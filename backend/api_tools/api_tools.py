import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access an environment variable
scopus_api_key = os.getenv('SCOPUS_APIKEY')
sciencedirect_api_key = os.getenv('SCIENCEDIRECT_APIKEY')
scopus_inst_token = os.getenv('SCOPUS_INSTTOKEN')


def parse_data_scopus(response):
    #get json data
    data = response.json()
    #get search-results object
    search_results = data.get('search-results', {})
    #get entries list
    articles = search_results.get('entry', [])
    return articles
