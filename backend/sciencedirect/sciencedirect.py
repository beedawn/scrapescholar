import requests

from api_tools.api_tools import sciencedirect_api_key, parse_data_scopus

# triggers for science direct endpoint
def request_api(query: str):
    #request data from science direct
    response = requests.get(f"https://api.elsevier.com/content/search/sciencedirect?query={query}&apiKey={sciencedirect_api_key}")
    articles= parse_data_scopus(response)
    #return entries to sciencedirect endpoint response
    returnList = []
    x = 0
   
    for article in articles:
        error = article.get('error')
        if error is None:
            links = article.get('link')
            if links:
                link = links[1].get('@href')
            else:
                link = ""        
            returnList.append({
                    'id':x,
                    'title':article.get('dc:title'), 
                    'link':link, 
                    'date':article.get('prism:coverDate'), 
                    'source': "Science Direct",
                    })
        x += 1
    return returnList