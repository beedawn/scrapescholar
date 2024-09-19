import requests
import os
import datetime
import json
import csv
import urllib.parse 
from urllib.parse import quote
from dotenv import load_dotenv
load_dotenv()

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
    def __init__(self, title = None, year = None, citedBy = None, link = None, abstract = None, documentType = None, 
                 source = None, evaluation = None, methodology = None, clarity = None, completeness = None, transparency = None):
        self.title = title
        self.year = year
        self.citedBy = citedBy
        self.link = link
        self.abstract = abstract
        self.documentType = documentType
        self.source = source
        self.evaluation = evaluation
        self.methodology = methodology
        self.clarity = clarity
        self.completeness = completeness
        self.transparency = transparency

#   Create Query Execute Function
def query_scopus_api(keywords, key, subject = "COMP", minYear = "2015",):
    #Keyword Builder
    keywordPhrase = ""

    for currentWord in keywords:
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
    subj = subject

    #Final Assembly
    getPhrase = "https://api.elsevier.com/content/search/scopus?" \
        + "apiKey=" + key \
        + "&query=" + keywordPhrase \
        + "&httpAccept=" + httpAccept \
        + "&view=" + view \
        + "&date=" + dateRange \
        + "&count=" + count \
        + "&sort=" + sort \
        + "&subj=" + subject
    return getPhrase

#   Create function to 'get' all elements needed for the front end and print results to a CSV
def load_json_scrape_results(json_data):        
    with open("search_results.csv", mode='w', newline='') as file:
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

#   ---main--- This is testing the variables that I will recieve from the front end


#  Access an environment variable for API Key
api_key = os.getenv("SCOPUS_APIKEY_TH")

#   QueryParameters - keywordList is user input, the rest will be static and unique to the scienceDirect parameters
researcherKeywordList = ["cybersecurity", "AND", "non profit", "OR", "charity"]     
subjectComp = "COMP"
minYear2015 = "2015"

#   Build Query
searchQuery = QueryParameters(keywords=researcherKeywordList, subject=subjectComp, minYear=minYear2015)
queryURL = query_scopus_api(searchQuery.keywords, api_key)
print(queryURL)
apiResponse = requests.get(queryURL)
jsonResults = apiResponse.json()

#   Store Results in Class
search_results = (load_json_scrape_results(jsonResults))
