from fastapi import FastAPI

from fastapi.testclient import TestClient

from app.main import app
from api_tools.api_tools import scopus_api_key
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url
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
        assert item["asbtract"] != ''
        assert len(item["abstract"]) > 0
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
