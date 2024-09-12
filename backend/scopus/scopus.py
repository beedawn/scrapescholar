import requests
import os
import datetime
import json
import csv
# from dotenv import load_dotenv
 

# Load environment variables from .env file
# load_dotenv()            

#Create QueryParameters class
class QueryParameters:
    def __init__(self, keywords = None, subject = None, minYear = None):
        if keywords is None:
            keywords = []
        self.keywords = keywords
        self.subject = subject
        self.minYear = minYear

#Create SearchResults class
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

#Create Query Execute Function
def query_scopus_api(keywords, key, subject = "COMP", minYear = "2015",):
    #Keyword Builder
    keywordPhrase = ""
    for currentWord in keywords:
        strippedWord = currentWord.strip()
        if ' ' in currentWord:
            strippedWordPlus = strippedWord.replace(" ", "+")
            keywordPhrase += strippedWordPlus
        else:
            keywordPhrase += strippedWord
        keywordPhrase += "%20"

    #Other Parameters
    httpAccept = "application/json"
    view = "STANDARD"                               #Note: COMPLETE view is inaccessible with a standard token
    today = datetime.date.today()
    currentYear = today.year
    dateRange = minYear + "-" + str(currentYear)
    count = "2"
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

def parse_json(json_data):
    data = json.loads(json_data)
    results = []
    for entry in data["search-results"]["entry"]:
        result = SearchResults(
            title = entry["dc:title"],
            year = entry["prism:coverDate"].split("-")[0],
            citedBy = entry["citedby-count"],
            link = next((link["@href"] for link in entry["link"] if link["@ref"] == "scopus"), None),
            abstract = None,       #Need to upgrade to view=COMPLETE (requires subscription?)
            documentType = entry["subtypeDescription"],
            source = entry["prism:publicationName"],
            evaluation=None,
            methodology=None,
            clarity=None,
            completeness=None,
            transparency=None
        )
        results.append(result)
    return results

#   ---main--- This is testing the variables that I will recieve from the front end


#  Access an environment variable for API Key
api_key = os.getenv('SCOPUS_APIKEY')
#api_key_th = "737eab5d80dc68fd8dbb744fcad411b9"    #This is Tristan's API key but should be deleted before merge for security

#   QueryParameters - keywordList is user input, the rest will be static and unique to the scienceDirect parameters
researcherKeywordList = ["cybersecurity", "AND", "non profit", "OR", "charity"]     
subjectComp = "COMP"
minYear2015 = "2015"

#   Build Query
searchQuery = QueryParameters(keywords=researcherKeywordList, subject=subjectComp, minYear=minYear2015)
queryURL = query_scopus_api(searchQuery.keywords, api_key_th)
print(queryURL)
apiResponse = requests.get(queryURL)
jsonResults = apiResponse.text

#   Store Results in Class
search_results = (parse_json(jsonResults))
for result in search_results:
    print(result.__dict__)

#   Create CSV file to make parsing easier? Export?
#   Code...
#   Code...
#   Code...
