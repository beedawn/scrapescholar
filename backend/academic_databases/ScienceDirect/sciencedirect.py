import requests
from api_tools.api_tools import sciencedirect_api_key as default_sciencedirect_api_key, parse_data_scopus
from academic_databases.SearchResult import SearchResult
from algorithm.algorithm_interface import algorithm_interface
from urllib.parse import quote, urlparse


def verify_api_key(api_key):
    response = requests.get(
        f"https://api.elsevier.com/content/search/sciencedirect?query=gene&apiKey={api_key}")
    if(response.status_code == 200):
        return True
    else:
        return False

def sanitize_link_sciencedirect(untrusted_link):
    parsed_untrusted_link = urlparse(untrusted_link)
    if parsed_untrusted_link.scheme == "https" and parsed_untrusted_link.netloc == "www.sciencedirect.com":
        trusted_link = untrusted_link
    else:
        trusted_link = "http://null"
    return trusted_link

def request_data(keywords: str, id: int, apiKey:str):
    sciencedirect_api_key = default_sciencedirect_api_key
    if apiKey != "" and apiKey is not None:
        print("using user api key science direct")
        if(verify_api_key(apiKey)):
            sciencedirect_api_key = apiKey

    response = requests.get(
        f"https://api.elsevier.com/content/search/sciencedirect?query={keywords}&apiKey={sciencedirect_api_key}")
    articles = parse_data_scopus(response)
    return_articles = []
    article_id = id
    for article in articles:
        error = article.get('error')
        if error is None:
            links = article.get('link')
            if links:
                link = links[1].get('@href')
                link = sanitize_link_sciencedirect(link)
            else:
                link = "No link found."
            article_title = article.get('dc:title')
            relevance_score = algorithm_interface(keywords, article_title)
            return_articles.append(SearchResult(
                article_id=article_id,
                title=article.get('dc:title'),
                link=link,
                date=article.get('prism:coverDate'),
                citedby=article.get('citedby-count'),
                source="ScienceDirect",
                color='red',
                relevance_score=relevance_score,
                abstract='',
                document_type=article.get("subtypeDescription", "Unknown"),
                evaluation_criteria='',
                methodology=0,
                clarity=0,
                completeness=0,
                transparency=0
            ))
        article_id += 1
    return return_articles, id, (response.status_code, "sciencedirect")
