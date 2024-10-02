from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from api_tools.api_tools import sciencedirect_api_key
from tests.unit.get_cookie import get_cookie
client = TestClient(app)
#todo
#get access token from login endpoint
#mimic cookie so that these tests will pass

base_url = "http://localhost:8000" 
session = get_cookie()
def test_sciencedirect_response_has_title_and_link():

    response = session.get(f"{base_url}/academic_data?keywords=test&academic_database=ScienceDirect")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert isinstance(item, dict)
        assert "title" in item
        assert isinstance(item["title"], str)
        assert "link" in item
        assert isinstance(item["link"], str)
        assert item["link"].startswith("http")


def test_sciencedirect_empty_response_is_empty():
    response = session.get(f"{base_url}/academic_data?keywords=abcdefg+AND+hijklmnop+AND+12345&academic_database=ScienceDirect")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) is 0


def test_sciencedirect_apiKey_env_is_filled():
    assert sciencedirect_api_key is not None
