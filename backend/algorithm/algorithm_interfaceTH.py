import time
#gets article title, article abstract, author keywords
from algorithmTH import algorithm
from algorithmTH import get_stems
from algorithmTH import clean
from algorithmTH import compare

keywords = "cybersecurity training awareness small organizations vulnerabilities risk"
article_title = "A quest for research and knowledge gaps in cybersecurity awareness for small and medium-sized enterprises"
article_abstract = "The proliferation of information and communication technologies in enterprises enables them to develop new business models and enhance their operational and commercial activities. Nevertheless, this practice also introduces new cybersecurity risks and vulnerabilities. This may not be an issue for large organizations with the resources and mature cybersecurity programs in place; the situation with small and medium-sized enterprises (SMEs) is different since they often lack the resources, expertise, and incentives to prioritize cybersecurity. In such cases, cybersecurity awareness can be a critical component of cyberdefense. However, research studies dealing with cybersecurity awareness or related domains exclusively for SMEs are rare, indicating a pressing need for research addressing the cybersecurity awareness requirements of SMEs. Prior to that, though, it is crucial to identify which aspects of cybersecurity awareness require further research in order to adapt or conform to the needs of SMEs. In this study, we conducted a systematic literature review that focused on cybersecurity awareness, prioritizing those performed with a particular focus on SMEs. The study seeks to analyze and evaluate such studies primarily to determine knowledge and research gaps in the cybersecurity awareness field for SMEs, thus providing a direction for future research."
authorKeywords = None


def algorithm_interface(keywords, article_title, article_abstract=None, authorkeywords=None):
    # relevance_score = dictionaryAlgorithm(article_title, keywords)
    relevance_score = 0
    keyword_stems = get_stems(keywords)
    
    if article_title is not None and article_abstract is not None:
        cleaned_title = clean(article_title)
        cleaned_abstract = clean(article_abstract)
        title_score = compare(cleaned_title, keyword_stems)
        abstract_score = compare(cleaned_abstract, keyword_stems)
        print("titel score")
        print(title_score)
        print("abstract score")
        print(abstract_score)
        relevance_score = (title_score[0] + abstract_score[0]) / (title_score[1] + abstract_score[1])
        return relevance_score
    if article_title is not None and article_abstract is None:
        cleaned_title = clean(article_title)
        title_score = compare(cleaned_title, keyword_stems)
        relevance_score = title_score[0] / title_score[1]
        print("title score")
        print(title_score)
        return(relevance_score)

start = time.time()
result = algorithm_interface(keywords, article_title, article_abstract, authorKeywords)
end = time.time()
print("Relevance Score: " + str(round(result*100, 2)) + "%")

timeAlgorithm = end - start
print("Algorithm Time: " + str(round(timeAlgorithm,4)) + " seconds")

