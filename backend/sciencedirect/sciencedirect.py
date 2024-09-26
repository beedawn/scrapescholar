import requests
import os
import datetime
import json
import csv
import urllib.parse 
import api_tools
from dotenv import load_dotenv
load_dotenv()

#   Create QueryParameters class
class QueryParameters:
    def __init__(self, keywords = None, minYear = None):
        if keywords is None:
            keywords = []
        self.keywords = keywords
        self.minYear = minYear

#   Create SearchResults class
class SearchResults:
    def __init__(self, title = None, year = None, link = None, source = None, relevanceScore = None):
        self.title = title
        self.year = year
        self.link = link
        self.source = source
        self.relevanceScore = relevanceScore

#   Create Query Execute Function
def query_science_direct_api(keywords, key, minYear):
    listKeywords = keywords.split(',')
    #Keyword Builder
    keywordPhrase = ""

    for currentWord in listKeywords:
        strippedWord = currentWord.strip()
        encodedWord = urllib.parse.quote(strippedWord).replace(" ", "+")
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
    key = key

    #Final Assembly
    getPhrase = "https://api.elsevier.com/content/search/sciencedirect?" \
        + "apiKey=" + key \
        + "&query=" + keywordPhrase \
        + "&httpAccept=" + httpAccept \
        + "&view=" + view \
        + "&date=" + dateRange \
        + "&count=" + count \
        + "&sort=" + sort
    return getPhrase

#   Create function to 'get' all elements needed for the front end and print results to a CSV
def json_to_csv(json_data):        
    file_path = "search_results_sciencedirect.csv"
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Title","Year","Link","Source","Relevancy Score"])
        for entry in json_data["search-results"].get("entry", []):
            # Find URL link before parsing the rest of the data
            for link in entry.get("link", []):
                if link.get("@ref") == "scidir":
                    href_value = link.get("@href")
            # Classify the remaining attributes
            result = SearchResults(
                title = entry.get("dc:title"),
                year = str(entry.get("prism:coverDate", "Not Listed")[:4]),
                link = href_value,
                source = "Science Direct",
                relevanceScore = "0%"
            )
            rowArray = [result.title, result.year, result.link, result.source, result.relevanceScore]
            writer.writerow(rowArray)
        file.close()
    return file_path

#  Access an environment variable for API Key
api_key = os.getenv("SCIENCEDIRECT_APIKEY")

#   QueryParameters - keywordList is user input, the rest will be static and unique to the scienceDirect parameters
# researcherKeywordList = ["cybersecurity", "AND", "non profit", "OR", "charity"]     
# minYear2015 = "2015"