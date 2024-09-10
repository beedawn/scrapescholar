import requests
import os
from dotenv import load_dotenv
 

# Load environment variables from .env file
load_dotenv()            

#Create QueryParameters class
class QueryParameters:
    def __init__(self, keywords = None, subject = None, minYear = None):
        if keywords is None:
            keywords = []
        self.keywords = keywords
        self.subject = subject
        self.minYear = minYear
    def __repr__(self):
        return (f"QueryParameters(keywords={self.keywords}, "
                f"subject={self.subject}, minYear={self.minYear})")

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
    def __repr__(self):
        return (f"SearchResults(title={self.title!r}, year={self.year!r}, citedBy={self.citedBy!r}, "
                f"link={self.link!r}, abstract={self.abstract!r}, documentType={self.documentType!r}, "
                f"source={self.source!r}, evaluation={self.evaluation!r}, methodology={self.methodology!r}, "
                f"clarity={self.clarity!r}, completeness={self.completeness!r}, transparency={self.transparency!r})")

# Triggers for science direct endpoint
def request_api(query: str):
    #request data from science direct
    response = requests.get(f"https://api.elsevier.com/content/search/sciencedirect?query={query}&apiKey={api_key}")
    #get json data
    data = response.json()
    #get search-results object
    search_results= data.get('search-results', {})
    #get entries list
    entries = search_results.get('entry',[])
    #return entries to sciencedirect endpoint response
 
    returnList = []
 
    for entry in entries:
        title = entry.get('dc:title')
        links = entry.get('link')
        link = links[1].get('@href')
        returnList.append({
            'title':title, 
            'link':link
            })
 
    return returnList


#   ---main---


#  Access an environment variable for API Key
api_key = os.getenv('SCIENCEDIRECT_APIKEY')
api_key = "737eab5d80dc68fd8dbb744fcad411b9"    #This is Tristan's API key but should be deleted before merge for security

#   QueryParameters - keywordList is user input, the rest will be static and unique to the scienceDirect parameters
researcherKeywordList = ["cybersecurity", "AND", "nonprofit"]     
subject = "COMP"
minYear = "2015"

#   Build Query



