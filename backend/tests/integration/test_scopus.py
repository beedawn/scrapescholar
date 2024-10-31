from fastapi import FastAPI

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from academic_databases.SearchResult import SearchResult
import pytest
from academic_databases.Scopus.scopus import request_data

from app.main import app
from api_tools.api_tools import scopus_api_key
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url

mock_scopus_response = {
    "search-results": {
        "opensearch:totalResults": "959738",
        "opensearch:startIndex": "0",
        "opensearch:itemsPerPage": "1",
        "opensearch:Query": {
            "@role": "request",
            "@searchTerms": "training",
            "@startPage": "0"
        },
        "link": [
            {
                "@_fa": "true",
                "@ref": "self",
                "@href": "https://api.elsevier.com/content/search/scopus?start=0&count=1&query=training&view=standard&date=1900-2024&sort=relevancy&subj=COMP",
                "@type": "application/json"
            },
            {
                "@_fa": "true",
                "@ref": "first",
                "@href": "https://api.elsevier.com/content/search/scopus?start=0&count=1&query=training&view=standard&date=1900-2024&sort=relevancy&subj=COMP",
                "@type": "application/json"
            },
            {
                "@_fa": "true",
                "@ref": "next",
                "@href": "https://api.elsevier.com/content/search/scopus?start=1&count=1&query=training&view=standard&date=1900-2024&sort=relevancy&subj=COMP",
                "@type": "application/json"
            },
            {
                "@_fa": "true",
                "@ref": "last",
                "@href": "https://api.elsevier.com/content/search/scopus?start=4999&count=1&query=training&view=standard&date=1900-2024&sort=relevancy&subj=COMP",
                "@type": "application/json"
            }
        ],
        "entry": [
            {
                "@_fa": "true",
                "link": [
                    {
                        "@_fa": "true",
                        "@ref": "self",
                        "@href": "https://api.elsevier.com/content/abstract/scopus_id/85206900643"
                    },
                    {
                        "@_fa": "true",
                        "@ref": "author-affiliation",
                        "@href": "https://api.elsevier.com/content/abstract/scopus_id/85206900643?field=author,affiliation"
                    },
                    {
                        "@_fa": "true",
                        "@ref": "scopus",
                        "@href": "https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85206900643&origin=inward"
                    },
                    {
                        "@_fa": "true",
                        "@ref": "scopus-citedby",
                        "@href": "https://www.scopus.com/inward/citedby.uri?partnerID=HzOxMe3b&scp=85206900643&origin=inward"
                    }
                ],
                "prism:url": "https://api.elsevier.com/content/abstract/scopus_id/85206900643",
                "dc:identifier": "SCOPUS_ID:85206900643",
                "eid": "2-s2.0-85206900643",
                "dc:title": "A Systematic and Meta-Analysis Review of Augmented Reality Interventions for Individuals with Autism Spectrum Disorder",
                "dc:creator": "Jacob U.S.",
                "prism:publicationName": "Ubiquitous Learning",
                "prism:issn": "18359795",
                "prism:volume": "17",
                "prism:issueIdentifier": "2",
                "prism:pageRange": "245-264",
                "prism:coverDate": "2024-12-30",
                "prism:coverDisplayDate": "30 December 2024",
                "prism:doi": "10.18848/1835-9795/CGP/v17i02/245-264",
                "citedby-count": "0",
                "affiliation": [
                    {
                        "@_fa": "true",
                        "affilname": "University of Johannesburg",
                        "affiliation-city": "Johannesburg",
                        "affiliation-country": "South Africa"
                    }
                ],
                "prism:aggregationType": "Journal",
                "subtype": "ar",
                "subtypeDescription": "Article",
                "source-id": "21100236814",
                "openaccess": "0",
                "openaccessFlag": "false"
            }
        ]
    }
}

@pytest.fixture
def setup_mock_scopus():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_scopus_response
        mock_get.return_value = mock_response
        yield mock_get

def test_mock_scopus(setup_mock_scopus):
    keywords = "training"
    id = 1
    key = scopus_api_key
    subject = "COMP"
    min_year = "1990"

    result_articles, article_id = request_data(keywords, id, key, subject, min_year)

    assert len(result_articles) == 1
    assert isinstance(result_articles[0], SearchResult)
    assert result_articles[0].article_id is not None
    assert result_articles[0].title == "A Systematic and Meta-Analysis Review of Augmented Reality Interventions for Individuals with Autism Spectrum Disorder"
    assert result_articles[0].link == "https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85206900643&origin=inward"
    assert result_articles[0].date == "2024-12-30"
    assert result_articles[0].citedby == "0"
    assert result_articles[0].source == "Scopus"
    assert result_articles[0].color is not None
    assert result_articles[0].relevance_score is not None
    assert result_articles[0].abstract is not None
    assert result_articles[0].document_type == "Article"
    assert result_articles[0].evaluation_criteria == ''
    assert result_articles[0].methodology == 0
    assert result_articles[0].clarity == 0
    assert result_articles[0].completeness == 0
    assert result_articles[0].transparency == 0


client = TestClient(app)
session = get_cookie()

def test_scopus_response_returns_correct_elements():
    response = session.get(f"{base_url}/academic_data?keywords=test&academic_database=Scopus")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["articles"], list)
    for item in data["articles"]:
        assert isinstance(item, dict)
        assert "article_id" in item
        assert isinstance(item["article_id"], int)    
        assert "title" in item
        assert isinstance(item["title"], str)
        assert "date" in item
        assert "citedby" in item
        assert "link" in item
        assert isinstance(item["link"], str)
        from urllib.parse import urlparse
        parsed_url = urlparse(item["link"])
        assert parsed_url.hostname and parsed_url.hostname.endswith(".scopus.com")
        assert "abstract" in item
        assert "document_type" in item
        assert "source" in item
        assert item["source"] == "Scopus"
        assert "evaluation_criteria" in item
        assert "color" in item
        assert item["color"] == "Not Relevant" or item["color"] == "SemiRelevant" or item["color"] == "Relevant" or item["color"] == ""
        assert "relevance_score" in item
        assert isinstance(item["relevance_score"], float)
        assert item["relevance_score"] >= 0 and item["relevance_score"] <= 100
    search_id=data["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
        
def test_scopus_student_rating_information_available():
    response = session.get(f"{base_url}/academic_data?keywords=test&academic_database=Scopus")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["articles"], list)
    for item in data["articles"]:
        assert "methodology" in item
        assert isinstance(item["methodology"], int)
        assert item["methodology"] >=0 & item["methodology"] <=1    #May need to change depending on if we implement different logic
        assert "clarity" in item
        assert isinstance(item["clarity"], int)
        assert item["clarity"] >=0 & item["clarity"] <=1
        assert "completeness" in item
        assert isinstance(item["completeness"], int)
        assert item["completeness"] >=0 & item["completeness"] <=1
        assert "transparency" in item
        assert isinstance(item["transparency"], int)
        assert item["transparency"] >=0 & item["transparency"] <=1
    search_id=data["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
        
def test_scopus_empty_response_is_empty():
    response = session.get(f"{base_url}/academic_data?keywords=abcdefg+AND+hijklmnop+AND+12345&academic_database=Scopus")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["articles"], list)
    assert len(data["articles"]) is 0
    search_id=data["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")

def test_scopus_apiKey_is_filled():
    assert scopus_api_key is not None




    