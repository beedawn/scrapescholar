import json

def load_json_scrape_results(json_data):
    search_results_list = []
    for entry in json_data:
        result = SearchResults(
            title = entry.get("dc:title"),
            year = entry.get("prism:coverDate")[:4],
            citedBy = entry.get("citedby-count"),
            link = next((link["@href"] for link in entry.get["link"] if link["@ref"] == "scopus"), None),
            abstract = None,       #Need to upgrade to view=COMPLETE (requires subscription?)
            documentType = entry.get("subtypeDescription"),
            source = "Scopus",
            evaluation=None,
            methodology=None,
            clarity=None,
            completeness=None,
            transparency=None
        )
        search_results_list.append(result)
    return search_results_list

# -- main --



with open('sample.json') as f:
   jsonData = json.load(f)

# print(jsonData)

# Title
for entry in jsonData["search-results"].get("entry", []):
    #Title
    title = entry.get("dc:title")
    print(title)

    #Year
    year = entry.get("prism:coverDate")[:4]
    print(year)

    #Link
    for link in entry.get("link", []):
        if link.get("@ref") == "scopus":
            href_value = link.get("@href")
            print(href_value)
    
    #CitedBy
    citedBy = entry.get("citedby-count")
    print(citedBy)

    #Abstract
    abstract = None
    print(abstract)

    #DocumentType
    documentType = entry.get("subtypeDescription")
    print(documentType)


