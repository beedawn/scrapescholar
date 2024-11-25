import requests
from api_tools.api_tools import sciencedirect_api_key as default_sciencedirect_api_key, parse_data_scopus
from academic_databases.SearchResult import SearchResult
from algorithm.algorithm_interface import algorithm_interface


def request_data(keywords: str, id: int, apiKey:str):
    if apiKey is not "" and apiKey is not None:
        print("using user api key science direct")
        sciencedirect_api_key = apiKey
    else:
        sciencedirect_api_key = default_sciencedirect_api_key
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
            else:
                link = ""
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
    return return_articles, id
