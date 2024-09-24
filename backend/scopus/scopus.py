import requests
import os
import datetime
import json
import csv
from urllib.parse import quote
import random

from dotenv import load_dotenv
load_dotenv()
from api_tools.api_tools import scopus_api_key, parse_data_scopus

#   Create QueryParameters class
class QueryParameters:
    def __init__(self, keywords = None, subject = None, minYear = None):
        if keywords is None:
            keywords = []
        self.keywords = keywords
        self.subject = subject
        self.minYear = minYear

#   Create SearchResults class
class SearchResults:
    def __init__(self, title = None, year = None, citedBy = None, link = None, abstract = None, documentType = None, source = None,
                 evaluation = None, relevanceScore = None, methodology = None, clarity = None, completeness = None, transparency = None):
        self.title = title
        self.year = year
        self.citedBy = citedBy
        self.link = link
        self.abstract = abstract
        self.documentType = documentType
        self.source = source
        self.evaluation = evaluation
        self.relevanceScore = relevanceScore
        self.methodology = methodology
        self.clarity = clarity
        self.completeness = completeness
        self.transparency = transparency

#   Create Query Execute Function
def query_scopus_api(keywords, key, subject, minYear):
    #Keyword Builder
    keywordPhrase = ""

    for currentWord in keywords:
        strippedWord = currentWord.strip()
        encodedWord = quote(strippedWord).replace(" ", "+")
        keywordPhrase += encodedWord
        keywordPhrase += "%20"

    #Other Parameters
    httpAccept = "application/json"
    view = "STANDARD"                               #Note: COMPLETE view is inaccessible with a standard token
    today = datetime.date.today()
    currentYear = today.year
    dateRange = minYear + "-" + str(currentYear)
    count = "25"
    sort = "relevancy"
    subj = subject
    key = key

    #Final Assembly
    built_query = "https://api.elsevier.com/content/search/scopus?" \
        + "apiKey=" + key \
        + "&query=" + keywordPhrase \
        + "&httpAccept=" + httpAccept \
        + "&view=" + view \
        + "&date=" + dateRange \
        + "&count=" + count \
        + "&sort=" + sort \
        + "&subj=" + subj
    
    response = requests.get(built_query)
    articles=parse_data_scopus(response)
    #return entries to scopus endpoint response
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
                    'color':'red',
                    'relevance': random.randint(1, 100),
                    'abstract':'',
                    'doctype':'',
                    'evaluation_criteria':'',
                    'color':'',
                    'methodology':0,
                    'clarity':0,
                    'completeness':0,
                    'transparency':0


                    })
        x += 1
    return return_articles






# csv stuff
#   Create function to 'get' all elements needed for the front end and print results to a CSV
def load_json_scrape_results(json_data):        
    file_path = "search_results.csv"
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Title","Year","Cited By","Link","Abstract","Document Type","Source","Evaluation","Methodology","Clarity","Completeness","Transparency"])
        for entry in json_data["search-results"].get("entry", []):
            # Find URL link before parsing the rest of the data
            for link in entry.get("link", []):
                if link.get("@ref") == "scopus":
                    href_value = link.get("@href")
            # Classify the remaining attributes
            result = SearchResults(
                title = entry.get("dc:title"),
                year = str(entry.get("prism:coverDate", "Not Listed")[:4]),
                citedBy = entry.get("citedby-count"),
                link = href_value,
                abstract = None,       #Need to upgrade to view=COMPLETE (requires subscription?)
                documentType = entry.get("subtypeDescription"),
                source = "Scopus",
                evaluation="0",
                methodology="0",
                clarity="0",
                completeness="0",
                transparency="0"
            )
            rowArray = [result.title, result.year, result.citedBy, result.link, str(result.abstract), result.documentType, 
                        result.source, result.evaluation, result.methodology, result.clarity, result.completeness, result.transparency]
            writer.writerow(rowArray)
        file.close()
    return file_path



#   QueryParameters - keywordList is user input, the rest will be static and unique to the scienceDirect parameters
# researcherKeywordList = ["cybersecurity", "AND", "non profit", "OR", "charity"]     
# subjectComp = "COMP"
# minYear2015 = "2015"