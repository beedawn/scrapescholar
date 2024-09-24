import requests
import datetime
import csv
import scopus.scopus as scopus
from urllib.parse import quote
import random
from api_tools.api_tools import scopus_api_key, parse_data_scopus

#   Create QueryParameters class
class QueryParameters:
    def __init__(self, keywords = None, subject = None, min_year = None):
        if keywords is None:
            keywords = []
        self.keywords = keywords
        self.subject = subject
        self.min_year = min_year

#   Create SearchResults class
class SearchResult:
    def __init__(self, id, title = None, date = None, citedby = None, link = None, abstract = None, document_type = None, source = None,
                 evaluation_criteria = None, color:str=None, relevance_score = None, methodology = None, clarity = None, completeness = None, transparency = None):
        self.id=id
        self.title = title
        self.date = date
        self.citedby = citedby
        self.link = link
        self.abstract = abstract
        self.document_type = document_type
        self.source = source
        self.evaluation_criteria = evaluation_criteria
        self.color = color
        self.relevance_score = relevance_score #relevance
        self.methodology = methodology
        self.clarity = clarity
        self.completeness = completeness
        self.transparency = transparency



#   Create Query Execute Function
def query_scopus_api(keywords, key: str=scopus.scopus_api_key, subject: str="", min_year: str="1900"):
    encoded_keywords = quote(keywords).replace(" ", "+")
    subject = quote(subject)
    min_year= quote(min_year)
    #Other Parameters
    http_accept = "application/json"
    view = "STANDARD"                               #Note: COMPLETE view is inaccessible with a standard token
    today = datetime.date.today()
    current_year = today.year
    date_range = min_year + "-" + str(current_year)
    count = "25"
    sort = "relevancy"
    subj = subject
    key = key

    #Final Assembly
    built_query = "https://api.elsevier.com/content/search/scopus?" \
        + "apiKey=" + key \
        + "&query=" + encoded_keywords \
        + "&httpAccept=" + http_accept \
        + "&view=" + view \
        + "&date=" + date_range \
        + "&count=" + count \
        + "&sort=" + sort \
        + "&subj=" + subj
    response = requests.get(built_query)
    articles=parse_data_scopus(response)
    #return entries to scopus endpoint response
    return_articles = []
    article_id = 0
    for article in articles:
        error = article.get('error')
        if error is None:
            links = article.get('link')
            if links:
                link = links[2].get('@href')
            else:
                link = ""
            return_articles.append(SearchResult(
                    id=article_id,
                    title=article.get('dc:title'), 
                    link=link, 
                    date=article.get('prism:coverDate'), 
                    citedby=article.get('citedby-count'),
                    source="Scopus",
                    color='red',
                    relevance_score=random.randint(1, 100),
                    abstract='',
                    document_type=article.get("subtypeDescription"),
                    evaluation_criteria='',
                    methodology=0,
                    clarity=0,
                    completeness=0,
                    transparency=0
                    ))
        article_id += 1
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
            result = SearchResult(
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