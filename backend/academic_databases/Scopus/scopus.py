import requests
import datetime
import csv
from urllib.parse import quote
import random
from api_tools.api_tools import scopus_api_key, scopus_inst_token, parse_data_scopus
from academic_databases.SearchResult import SearchResult

from typing import List
from algorithm.algorithm_interface import algorithm_interface

def request_data(keywords: str, id: int, key: str = scopus_api_key, subject: str = "", min_year: str = "1900"):
    if scopus_inst_token is not None:
        print("SCOPUS INST TOKEN")
        encoded_keywords = quote(keywords)
        subject = quote(subject)
        min_year = quote(min_year)
        # Other Parameters
        http_accept = "application/json"
        view = "COMPLETE"  # Note: COMPLETE view is needed to view abstract
        today = datetime.date.today()
        current_year = today.year
        date_range = min_year + "-" + str(current_year)
        count = "25"
        sort = "relevancy"
        insttoken = scopus_inst_token

        built_query = "https://api.elsevier.com/content/search/scopus?" \
                      + "apiKey=" + key \
                      + "&query=" + encoded_keywords \
                      + "&httpAccept=" + http_accept \
                      + "&view=" + view \
                      + "&date=" + date_range \
                      + "&count=" + count \
                      + "&sort=" + sort \
                      + "&subj=" + subject \
                      + "&insttoken=" + insttoken
    else:
        encoded_keywords = quote(keywords)
        subject = quote(subject)
        min_year = quote(min_year)
        # Other Parameters
        http_accept = "application/json"
        view = "STANDARD"  # Note: COMPLETE view is inaccessible with a standard token
        today = datetime.date.today()
        current_year = today.year
        date_range = min_year + "-" + str(current_year)
        count = "25"
        sort = "relevancy"
        print("Scopus inst token not found")
        built_query = "https://api.elsevier.com/content/search/scopus?" \
                      + "apiKey=" + key \
                      + "&query=" + encoded_keywords \
                      + "&httpAccept=" + http_accept \
                      + "&view=" + view \
                      + "&date=" + date_range \
                      + "&count=" + count \
                      + "&sort=" + sort \
                      + "&subj=" + subject

    response = requests.get(built_query)
    articles = parse_data_scopus(response)
    #return entries to scopus endpoint response
    return_articles: List[SearchResult] = []
    article_id = id
    for article in articles:
        error = article.get('error')
        if error is None:
            links = article.get('link')
            if links:
                link = links[2].get('@href')
            else:
                link = ""

                # could be refactored into its ownfunction
            article_title = article.get('dc:title')

            relevance_score = algorithm_interface(keywords, article_title)

            # end refactoring
            return_articles.append(SearchResult(
                article_id=article_id,
                title=article_title,
                link=link,
                date=article.get('prism:coverDate'),
                citedby=article.get('citedby-count'),
                source="Scopus",
                color='red',
                relevance_score=random.randint(1, 100),
                abstract=article.get('dc:description'),
                document_type=article.get('subtypeDescription'),
                evaluation_criteria='',
                methodology=0,
                clarity=0,
                completeness=0,
                transparency=0
            ))
        article_id += 1
    return return_articles, article_id
