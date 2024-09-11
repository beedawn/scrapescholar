from fastapi import FastAPI

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_sciencedirect_response_has_title_and_link():
    response = client.get("/sciencedirect?query=test")
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


def test_sciencedirect_empty_response_is_empty():
    response = client.get("/sciencedirect?query=abcdefg+AND+hijklmnop+AND+12345")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data,list)

    assert len(data) is 0   




    
  
