import requests
import os
from dotenv import load_dotenv

load_dotenv()    
api_key = os.getenv('SCIENCEDIRECT_APIKEY')
# Triggers for science direct endpoint
def request_api(query: str):
    #request data from science direct
    response = requests.get(f"https://api.elsevier.com/content/search/sciencedirect?httpAccept=application/xml&query={query}&apiKey={api_key}")
    #get json data
    data = response.json()
    #get search-results object
    search_results= data.get('search-results', {})
    #get entries list
    entries = search_results.get('entry',[])
    #return entries to sciencedirect endpoint response
    returnList =[]
    for entry in entries:
        title = entry.get('dc:title')
        links = entry.get('link')
        link = links[1].get('@href')
        returnList.append({
            'title':title, 
            'link':link
            })
 
    return returnList



