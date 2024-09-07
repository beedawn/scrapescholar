import requests
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Access an environment variable
api_key = os.getenv('SCIENCEDIRECT_APIKEY')

def request_api():

    response = requests.get(f"https://api.elsevier.com/content/search/sciencedirect?query=gene&apiKey={api_key}")

    return response.json()
