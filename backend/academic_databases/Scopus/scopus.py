import requests
import datetime
import csv
from urllib.parse import quote, urlparse
import random
from api_tools.api_tools import scopus_api_key, scopus_inst_token, parse_data_scopus
from academic_databases.SearchResult import SearchResult

from typing import List
from algorithm.algorithm_interface import algorithm_interface


def verify_api_key(api_key):
    response = requests.get(
        f"https://api.elsevier.com/content/search/scopus?query=all(gene)&apiKey={api_key}")
    if(response.status_code == 200):
        return True
    else:
        return False

def sanitize_link_scopus(untrusted_link):
    parsed_untrusted_link = urlparse(untrusted_link)
    if parsed_untrusted_link.scheme == "https" and parsed_untrusted_link.netloc == "www.scopus.com" and parsed_untrusted_link.path == "/inward/record.uri":
        trusted_link = untrusted_link
    else:
        trusted_link = "Potentially malicious link detected. Blocked for user safety."
    return trusted_link


def request_data(keywords: str, id: int, apiKey: str= None, key: str = scopus_api_key, subject: str = "",
                 min_year: str = "1900"):
    if apiKey is not "" and apiKey is not None:
        print("using user api key scopus")
        if(verify_api_key(apiKey)):
            key = apiKey
    if scopus_inst_token is not None:
        encoded_keywords = quote(keywords)
        subject = quote(subject)
        min_year = quote(min_year)
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
        http_accept = "application/json"
        view = "STANDARD"  # Note: COMPLETE view is inaccessible with a standard token
        today = datetime.date.today()
        current_year = today.year
        date_range = min_year + "-" + str(current_year)
        count = "25"
        sort = "relevancy"
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
    return_articles: List[SearchResult] = []
    article_id = id
    for article in articles:
        error = article.get('error')
        if error is None:
            links = article.get('link')
            if links:
                link = links[2].get('@href')
                #Sanitize Link
                sanitized_link = sanitize_link_scopus(link)
            else:
                sanitized_link = "No link found."

            article_title = article.get('dc:title')
            article_abstract = article.get('dc:description')
            algorithm_score = 0

            # could be turned on to scan abstract, makes response super slow
            # if article_abstract is not None:
            #     algorithm_score = algorithm_interface(article_abstract, article_abstract)

            relevance_score = algorithm_interface(keywords, article_title)
            # useless without lines 88-90 uncommented, but response is EXTREMELY SLOW
            if algorithm_score > 0:
                relevance_score = (relevance_score + algorithm_score) / 2
            return_articles.append(SearchResult(
                article_id=article_id,
                title=article_title,
                link=sanitized_link,
                date=article.get('prism:coverDate'),
                citedby=article.get('citedby-count'),
                source="Scopus",
                color='red',
                relevance_score=relevance_score,
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
