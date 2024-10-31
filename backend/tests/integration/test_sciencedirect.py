from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from academic_databases.SearchResult import SearchResult
from app.main import app
from api_tools.api_tools import sciencedirect_api_key
from academic_databases.ScienceDirect.sciencedirect import request_data

# client = TestClient(app)
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url

session = get_cookie()


# def test_sciencedirect_response_returns_correct_elements():
#     response = session.get(f"{base_url}/academic_data?keywords=test&academic_database=ScienceDirect")
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data["articles"], list)
#     for item in data["articles"]:
#         assert isinstance(item, dict)
#         assert "article_id" in item
#         assert isinstance(item["article_id"], int)
#         assert "title" in item
#         assert isinstance(item["title"], str)
#         assert "date" in item
#         assert "citedby" in item
#         assert "link" in item
#         assert isinstance(item["link"], str)
#         from urllib.parse import urlparse
#         parsed_url = urlparse(item["link"])
#         assert parsed_url.hostname and parsed_url.hostname.endswith(".sciencedirect.com")
#         assert "abstract" in item
#         assert "document_type" in item
#         assert "source" in item
#         assert item["source"] == "ScienceDirect"
#         assert "evaluation_criteria" in item
#         assert "color" in item
#         assert item["color"] == "Not Relevant" or item["color"] == "SemiRelevant" or item["color"] == "Relevant" or \
#                item["color"] == ""
#         assert "relevance_score" in item
#         assert isinstance(item["relevance_score"], float)
#         assert 0 <= item["relevance_score"] <= 100

#     search_id = data["search_id"]
#     session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")

# def test_sciencedirect_student_rating_information_available():
#     response = session.get(f"{base_url}/academic_data?keywords=test&academic_database=ScienceDirect")
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data["articles"], list)
#     for item in data["articles"]:
#         assert "methodology" in item
#         assert isinstance(item["methodology"], int)
#         assert item["methodology"] >= 0 & item[
#             "methodology"] <= 1  #May need to change depending on if we implement different logic
#         assert "clarity" in item
#         assert isinstance(item["clarity"], int)
#         assert item["clarity"] >= 0 & item["clarity"] <= 1
#         assert "completeness" in item
#         assert isinstance(item["completeness"], int)
#         assert item["completeness"] >= 0 & item["completeness"] <= 1
#         assert "transparency" in item
#         assert isinstance(item["transparency"], int)
#         assert item["transparency"] >= 0 & item["transparency"] <= 1
#     search_id = data["search_id"]
#     session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")

# def test_sciencedirect_empty_response_is_empty():
#     response = session.get(
#         f"{base_url}/academic_data?keywords=abcdefg+AND+hijklmnop+AND+12345&academic_database=ScienceDirect")
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data["articles"], list)
#     assert len(data["articles"]) == 0
#     search_id = data["search_id"]
#     session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")

def test_sciencedirect_apiKey_env_is_filled():
    assert sciencedirect_api_key is not None

mock_sciencedirect_response = {
    "search-results": {
        "opensearch:totalResults": "16293",
        "opensearch:startIndex": "0",
        "opensearch:itemsPerPage": "1",
        "opensearch:Query": {
            "@role": "request",
            "@searchTerms": "cybersecurity",
            "@startPage": "0"
        },
        "link": [
            {
                "@_fa": "true",
                "@ref": "self",
                "@href": "https://api.elsevier.com/",
                "@type": "application/json"
            },
            {
                "@_fa": "true",
                "@ref": "first",
                "@href": "https://api.elsevier.com/",
                "@type": "application/json"
            },
            {
                "@_fa": "true",
                "@ref": "next",
                "@href": "https://api.elsevier.com/",
                "@type": "application/json"
            },
            {
                "@_fa": "true",
                "@ref": "last",
                "@href": "https://api.elsevier.com/",
                "@type": "application/json"
            }
        ],
        "entry": [
            {
                "@_fa": "true",
                "load-date": "2024-10-11T00:00:00.000Z",
                "link": [
                    {
                        "@_fa": "true",
                        "@ref": "self",
                        "@href": "https://api.elsevier.com/content/article/pii/S2451958824001349"
                    },
                    {
                        "@_fa": "true",
                        "@ref": "scidir",
                        "@href": "https://www.sciencedirect.com/science/article/pii/S2451958824001349?dgcid=api_sd_search-api-endpoint"
                    }
                ],
                "dc:identifier": "DOI:10.1016/j.chbr.2024.100501",
                "prism:url": "https://api.elsevier.com/content/article/pii/S2451958824001349",
                "dc:title": "Cybersecurity activities for education and curriculum design: A survey",
                "dc:creator": "Muhusina Ismail",
                "prism:publicationName": "Computers in Human Behavior Reports",
                "prism:volume": "16",
                "prism:coverDate": "2024-12-31",
                "prism:startingPage": "100501",
                "prism:doi": "10.1016/j.chbr.2024.100501",
                "openaccess": "true",
                "pii": "S2451958824001349",
                "authors": {
                    "author": [
                        {
                            "$": "Muhusina Ismail"
                        },
                        {
                            "$": "Nisha Thorakkattu Madathil"
                        },
                        {
                            "$": "Djedjiga Mouheb"
                        }
                    ]
                }
            }
        ]
    }
}

@patch('requests.get')
def test_mock_sciencedirect(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = mock_sciencedirect_response
    mock_get.return_value = mock_response

    query = "test"
    start_id = 1
    result_articles, last_id = request_data(query, start_id)

    print("is it working?")
    assert len(result_articles) == 1
    assert isinstance(result_articles[0], SearchResult)
    assert result_articles[0].article_id
    assert result_articles[0].title == "Cybersecurity activities for education and curriculum design: A survey"
    assert result_articles[0].link == "https://www.sciencedirect.com/science/article/pii/S2451958824001349?dgcid=api_sd_search-api-endpoint"
    assert result_articles[0].date == "2024-12-31"
    assert result_articles[0].citedby == ''
    assert result_articles[0].source == "ScienceDirect"
    assert result_articles[0].color == "red"
    assert result_articles[0].relevance_score
    assert result_articles[0].abstract == ''
    assert result_articles[0].document_type == "Unknown"
    assert result_articles[0].evaluation_criteria == ''
    assert result_articles[0].methodology == 0
    assert result_articles[0].clarity == 0
    assert result_articles[0].completeness == 0
    assert result_articles[0].transparency == 0

