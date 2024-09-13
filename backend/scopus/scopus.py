import requests

from urllib.parse import quote

from api_tools.api_tools import scopus_api_key,parse_data_scopus
        
                         


# triggers for science direct endpoint
def request_api(query: str):
    #request data from science direct
    query=quote(query)
    response = requests.get(f"https://api.elsevier.com/content/search/scopus?query={query}&apiKey={scopus_api_key}")
    articles=parse_data_scopus(response)
    #return entries to sciencedirect endpoint response
    return_articles = []
    x = 0
    for article in articles:
        error = article.get('error')
        if error is None:
            links = article.get('link')
            if links:
                link = links[2].get('@href')
            else:
                link = ""
            return_articles.append({
                    'id':x,
                    'title': article.get('dc:title'), 
                    'link':link, 
                    'date':article.get('prism:coverDate'), 
                    'citedby': article.get('citedby-count'),
                    'source': "Scopus",
                    })
        x += 1
    return return_articles