import time
#gets article title, article abstract, author keywords
from algorithmTH import algorithm

keywords = "cool"
article_title = "Cybersecurity is cool!"
# article_title = "The proliferation of information and communication technologies in enterprises enables them to develop new business models and enhance their operational and commercial activities. Nevertheless, this practice also introduces new cybersecurity risks and vulnerabilities. This may not be an issue for large organizations with the resources and mature cybersecurity programs in place; the situation with small and medium-sized enterprises (SMEs) is different since they often lack the resources, expertise, and incentives to prioritize cybersecurity. In such cases, cybersecurity awareness can be a critical component of cyberdefense. However, research studies dealing with cybersecurity awareness or related domains exclusively for SMEs are rare, indicating a pressing need for research addressing the cybersecurity awareness requirements of SMEs. Prior to that, though, it is crucial to identify which aspects of cybersecurity awareness require further research in order to adapt or conform to the needs of SMEs. In this study, we conducted a systematic literature review that focused on cybersecurity awareness, prioritizing those performed with a particular focus on SMEs. The study seeks to analyze and evaluate such studies primarily to determine knowledge and research gaps in the cybersecurity awareness field for SMEs, thus providing a direction for future research."
article_abstract = None
authorKeywords = None


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

start = time.time()
result = algorithm_interface(keywords, article_title, article_abstract, authorKeywords)
end = time.time()
print("Relevance Score: " + str(result))

timeAlgorithm = end - start
print("Algorithm Time: " + str(round(timeAlgorithm,4)) + " seconds")

