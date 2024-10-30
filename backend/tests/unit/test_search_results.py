from academic_databases.SearchResult import SearchResult



def test_search_result_initialization():
    testResult = SearchResult(
        article_id = 1,
        title = "A quest for research and knowledge gaps in cybersecurity awareness for small and medium-sized enterprises",
        date = "2024-10-27",
        citedby = 10,
        link = "https://www.sciencedirect.com/science/article/pii/S157401372300059X",
        abstract = "The proliferation of information and communication technologies in enterprises enables them to develop new business models...",
        document_type = "Journal",
        source = "Scopus",
        evaluation_criteria = "accept",
        color = "green",
        relevance_score = 96,
        methodology = 1,
        clarity = 1,
        completeness = 1,
        transparency = 1
    )

    assert testResult.article_id == 1
    assert testResult.title == "A quest for research and knowledge gaps in cybersecurity awareness for small and medium-sized enterprises"
    assert testResult.date == "2024-10-27"
    assert testResult.citedby == 10
    assert testResult.link == "https://www.sciencedirect.com/science/article/pii/S157401372300059X"
    assert testResult.abstract == "The proliferation of information and communication technologies in enterprises enables them to develop new business models..."
    assert testResult.document_type == "Journal"
    assert testResult.source == "Scopus"
    assert testResult.evaluation_criteria == "accept"
    assert testResult.color == "green"
    assert testResult.relevance_score == 96
    assert testResult.methodology == 1
    assert testResult.clarity == 1
    assert testResult.completeness == 1
    assert testResult.transparency == 1


def test_search_result_initialization_optional_fields():
    testResult = SearchResult(
    article_id = 2
    )
    
    assert testResult.article_id == 2
    assert testResult.title is None
    assert testResult.date is None
    assert testResult.citedby is None
    assert testResult.link is None
    assert testResult.abstract is None
    assert testResult.document_type is None
    assert testResult.source is None
    assert testResult.evaluation_criteria is None
    assert testResult.color is None
    assert testResult.relevance_score is None
    assert testResult.methodology is None
    assert testResult.clarity is None
    assert testResult.completeness is None
    assert testResult.transparency is None