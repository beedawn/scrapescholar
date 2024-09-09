from fastapi import FastAPI

from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_read_main():
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


    assert len(data) > 0 


    
  
