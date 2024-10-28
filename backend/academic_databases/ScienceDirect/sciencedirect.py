import requests
import random

from api_tools.api_tools import sciencedirect_api_key, parse_data_scopus
from academic_databases.SearchResult import SearchResult
from algorithm.algorithm import algorithm

# triggers for science direct endpoint
def request_data(query: str, id: int):
    #request data from science direct
    response = requests.get(
        f"https://api.elsevier.com/content/search/sciencedirect?query={query}&apiKey={sciencedirect_api_key}")
    articles = parse_data_scopus(response)
    #return entries to sciencedirect endpoint response
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

            # could be refactored into its ownfunction
            article_title = article.get('dc:title')
            # needs updated to get article
            article_abstract = None
            title_score = algorithm(article_title, query)
            print("TITLE SCORE SCIENCE DIRECT")
            print(title_score)
            abstract_score = algorithm(article_title, query)
            relevance_score = 0
            if article_title is not None and article_abstract is not None:
                relevance_score = (title_score + abstract_score) / 2
            if article_title is not None and article_abstract is None:
                relevance_score = title_score

            # end refactoring
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
