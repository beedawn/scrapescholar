#   Create SearchResults class
class SearchResult:
    def __init__(self, article_id: int, title: str = None, date: str = None, citedby: int = None, link: str = None,
                 abstract: str = None, document_type: str = None, source: str = None,
                 evaluation_criteria: str = None, color: str = None, relevance_score: int = None,
                 methodology: int = None, clarity: int = None, completeness: int = None, transparency: int = None):
        self.article_id = article_id
        self.title = title
        self.date = date
        self.citedby = citedby
        self.link = link
        self.abstract = abstract
        self.document_type = document_type
        self.source = source
        self.evaluation_criteria = evaluation_criteria
        self.color = color
        self.relevance_score = relevance_score  #relevance
        self.methodology = methodology
        self.clarity = clarity
        self.completeness = completeness
        self.transparency = transparency
