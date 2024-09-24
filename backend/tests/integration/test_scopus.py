from fastapi import FastAPI

from fastapi.testclient import TestClient

from app.main import app
from scopus.scopus import scopus_api_key

client = TestClient(app)


def test_scopus_response_has_title_and_link():
    response = client.get("/keywords?query=test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data,list)

    for item in data:

        assert isinstance(item, dict)

        assert 'title' in item
        assert isinstance(item['title'], str)

        assert 'link' in item
        assert isinstance(item['link'], str)
        assert item['link'].startswith('http')


def test_scopus_empty_response_is_empty():
    response = client.get("/scopus?keywords=abcdefg+AND+hijklmnop+AND+12345")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data,list)

    assert len(data) is 0   


def test_scopus_apiKey_is_filled():

    assert scopus_api_key is not None



    
  
