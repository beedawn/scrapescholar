#gets article title, article abstract, author keywords
from algorithm.algorithm import algorithm


def algorithm_interface(keywords, article_title, article_abstract=None, authorkeywords=None):
    title_score = algorithm(article_title, keywords)
    relevance_score = 0
    if article_title is not None and article_abstract is not None:
        abstract_score = algorithm(article_title, keywords)
        relevance_score = (title_score + abstract_score) / 2
    if article_title is not None and article_abstract is None:
        relevance_score = title_score

    return round(relevance_score * (100/325), 0)
#325 is the max score returned by algorithm
