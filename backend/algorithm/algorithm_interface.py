#gets article title, article abstract, author keywords
from algorithm.algorithm import algorithm


def algorithm_interface(keywords, article_title, article_abstract=None):
    keywords = keywords.split(" ")
    skip_next = False
    new_keywords = []
    #filters out NOT, AND, OR and skips words after NOT to make algorithm more accurate and faster
    for keyword in keywords:
        if skip_next:
            skip_next = False
            continue

        elif keyword == "NOT":
            skip_next = True
            continue
        elif keyword == "AND":
            continue
        elif keyword == "OR":
            continue
        new_keywords.append(keyword)
    keywords = " ".join(new_keywords)
    title_score = algorithm(article_title, keywords)
    relevance_score = 0
    if article_title is not None and article_abstract is not None:
        abstract_score = algorithm(article_title, keywords)
        relevance_score = (title_score + abstract_score) / 2
    if article_title is not None and article_abstract is None:
        relevance_score = title_score

    return round(relevance_score * (100 / 325), 0)
#325 is the max score returned by algorithm
