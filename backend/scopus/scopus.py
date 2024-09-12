import requests
import os
import datetime
import json
import csv
## not sure why this is commented?
# from dotenv import load_dotenv
 

# Load environment variables from .env file
## not sure why this is commented?
# load_dotenv()            

## I don't think we need this?
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

    ## its hard to tell what this does
    ## it looks like it strips spaces off the ends of both sides of a keyword
    ## then checks currentWord if it has spaces
    ## then if currentWord has spaces, it replaces spaces in strippedWord with +
    ## then appends strippedWordPlus to keywordPhrase
    ## or if there aren't spaces then it appends the word to keyword phrase?
    ## would it be simpler to do keywords.replace(" ", "%20")??
    ## i mostly say this because im worried if someone searched "non profit" what would come out?
    ## i tried it and it gives me "non+profit%20" when i think it should be "non%20profit+"?
    ## something like:
    ## keywordPhrase = '+'.join(keywords).strip().replace(" ", "%20")

    ## but something better to avoid injection would be
    ## from urllib.parse import quote
    ## keywordPhrase = quote('+'.join(keywords).strip())
    ## this would convert all characters to url encoding and likely harden security

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

## maybe this should have a different name, like "json_to_search_results" or "classify_results"
## or something as it seems it does more than just parse json
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
   #This is Tristan's API key but should be deleted before merge for security
   ##should be stored in .env file

#   QueryParameters - keywordList is user input, the rest will be static and unique to the scienceDirect parameters
researcherKeywordList = ["cybersecurity", "AND", "non profit", "OR", "charity"]     
subjectComp = "COMP"
minYear2015 = "2015"

#   Build Query
## I don't think we need to store the keywords in an object, just the article info
searchQuery = QueryParameters(keywords=researcherKeywordList, subject=subjectComp, minYear=minYear2015)
queryURL = query_scopus_api(searchQuery.keywords, api_key_th)
print(queryURL)
apiResponse = requests.get(queryURL)
## could we just use .json instead? if we did then we could probably delete line 98
jsonResults = apiResponse.text

#   Store Results in Class
search_results = (parse_json(jsonResults))
for result in search_results:
    print(result.__dict__)

#   Create CSV file to make parsing easier? Export?
#   Code...
#   Code...
#   Code...
