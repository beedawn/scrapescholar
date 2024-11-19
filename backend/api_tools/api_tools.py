def parse_data_scopus(response):
    data = response.json()
    search_results = data.get('search-results', {})
    articles = search_results.get('entry', [])
    return articles
