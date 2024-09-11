import requests
import os
from dotenv import load_dotenv
 
# Load environment variables from .env file
load_dotenv()            
                         
# Access an environment variable
api_key = os.getenv('SCOPUS_APIKEY')

# triggers for science direct endpoint
def request_api(query: str):
    #request data from science direct
    response = requests.get(f"https://api.elsevier.com/content/search/scopus?query={query}&apiKey={api_key}")
    #get json data
    data = response.json()
    print(data)
    #get search-results object
    search_results= data.get('search-results', {})
    #get entries list
    entries = search_results.get('entry',[])
    #return entries to sciencedirect endpoint response
    returnList = []
    x = 0
   
    for entry in entries:
        error = entry.get('error')
        if error is None:
            title = entry.get('dc:title')
            links = entry.get('link')


            if links:
                link = links[1].get('@href')
            else:
                link = ""
            date = entry.get('prism:coverDate')
        
            returnList.append({
                    'id':x,
                    'title':title, 
                    'link':link, 
                    'date':date, 
                    'source': "Scopus",
                    })
        x += 1
    print(returnList)
    return returnList




