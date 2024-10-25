import requests
import datetime
from urllib.parse import quote

def proprietary_relevance_score(title, abstract, author_keywords, cited_by, year, search_keywords):
    # Determine if author keywords are available
    if author_keywords:
        TITLE_WEIGHT = 0.35
        ABSTRACT_WEIGHT = 0.30
        KEYWORDS_WEIGHT = 0.20
        YEAR_WEIGHT = 0.10
        CITED_BY_WEIGHT = 0.05
    else:
        TITLE_WEIGHT = 0.425
        ABSTRACT_WEIGHT = 0.425
        YEAR_WEIGHT = 0.10
        CITED_BY_WEIGHT = 0.05

    current_year = datetime.date.today().year

    # Helper functions
    def keyword_match_score(text, keywords):
        matches = sum(1 for kw in keywords if kw.lower() in text.lower())
        print("matches")
        print(matches / (len(keywords) / 2))
        return min(1, matches / (len(keywords) / 2)) if keywords else 0                 #Ignore characters that are less than 4? 5? chars
        # total_matches = sum(text.lower().count(kw.lower()) for kw in keywords)
        # print("Total matches:", total_matches /len(keywords) / 4)
        # return total_matches / len(keywords) /4 if keywords else 0

    def year_score(year):
        years_diff = current_year - int(year)
        print("year score")
        print(max(0, 1 - (years_diff * 0.1)))
        return max(0, 1 - (years_diff * 0.1))  # Deduct 10% for every year older than current year

    def cited_by_score(cited_by):
        print("cited by score")
        print(min(1, cited_by / 10))
        return min(1, cited_by / 10)  # Simple scaling; maxes out at 10 citations

    # Calculate individual scores
    title_score = keyword_match_score(title, search_keywords) * TITLE_WEIGHT
    abstract_score = keyword_match_score(abstract, search_keywords) * ABSTRACT_WEIGHT

    # Only add keywords score if available
    if author_keywords:
        print("author keywords match")
        print(author_keywords.replace(" | "," "))
        keywords_score = keyword_match_score(author_keywords.replace(" | "," "), search_keywords) * KEYWORDS_WEIGHT
    else:
        keywords_score = 0

    year_score_value = year_score(year) * YEAR_WEIGHT
    cited_by_score_value = cited_by_score(int(cited_by)) * CITED_BY_WEIGHT

    # Total relevance score (out of 100%)
    total_score = (title_score + abstract_score + keywords_score +
                   year_score_value + cited_by_score_value) * 100
    return round(total_score, 0)

def request_data(keywords: list = ["Cybersecurity", "AND", "Cyber Awareness", "AND", "Training", "AND", "nonprofit", "AND", "public organization"], key: str = "737eab5d80dc68fd8dbb744fcad411b9", subject: str = "COMP", min_year: str = "1900"):
    # print("keywords")
    # print(keywords)
    encoded_list = []
    for item in keywords:
        new_item = item.replace(" ", "+")
        encoded_list.append(new_item)
    # print("encoded list")
    # print(encoded_list)
    subject = quote(subject)
    min_year = quote(min_year)
    
    # Other Parameters
    http_accept = "application/json"
    view = "COMPLETE"
    today = datetime.date.today()
    current_year = today.year
    date_range = min_year + "-" + str(current_year)
    count = "25"  # Fetching 5 results for simplicity
    sort = "relevancy"
    insttoken = "eb52bd45804e5947070ad23d9bbd4d11"
    encoded_query = ""
    for element in encoded_list:
        encoded_query += element
        encoded_query += "%20"

    built_query = f"https://api.elsevier.com/content/search/scopus?apiKey={key}&query={encoded_query}&httpAccept={http_accept}&view={view}&date={date_range}&count={count}&sort={sort}&subj={subject}&insttoken={insttoken}"
    # print(built_query)
    response = requests.get(built_query)    
    data = response.json().get('search-results', {}).get('entry', [])
    
    article_id = 1
    for article in data:
        title = article.get('dc:title')
        abstract = article.get('dc:description')
        author_keywords = article.get('authkeywords', [])
        cited_by = article.get('citedby-count', 0)
        year = article.get('prism:coverDate', '0').split("-")[0]

        relevance_score = proprietary_relevance_score(
            title=title,
            abstract=abstract,
            author_keywords=author_keywords,
            cited_by=cited_by,
            year=year,
            search_keywords=keywords[::2]   # Assuming every other element
        )

        print(f"Article {article_id}:")
        print(f"Title: {title}")
        print(f"Abstract: {abstract}")
        print(f"Author Keywords: {author_keywords}")
        print(f"Cited By: {cited_by}")
        print(f"Year Published: {year}")
        print(f"Relevance Score: {relevance_score}%")
        print("-" * 50)

        article_id += 1

# Testing the function
request_data()
