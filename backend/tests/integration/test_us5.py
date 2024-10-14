from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from api_tools.api_tools import sciencedirect_api_key
client = TestClient(app)
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url
import pytest
session = get_cookie()

#UT-5.2

def test_user_data_slash_update_put():
    data = {
    "article_id": 1,
    "relevancy_color": "Not Relevant"
    }
    searchdata=session.get(f"{base_url}/academic_data?keywords=test&academic_database=Scopus")
    session.put(f"{base_url}/user_data/update", json=data)
    searchdata=searchdata.json()

    response = session.get(f"{base_url}/search/user/articles?search_id=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        print(item)
        if item["article_id"]==1:
            assert item["color"] == "Not Relevant" 
    search_id=searchdata["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")

