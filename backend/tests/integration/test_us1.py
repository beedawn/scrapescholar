from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from api_tools.api_tools import sciencedirect_api_key
client = TestClient(app)
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url
import pytest
session = get_cookie()

#UT-1.2

def test_user_data_slash_relevant_results():
    data = {
    "article_id": 1,
    "relevancy_color": "Not Relevant"
    }
    searchdata=session.get(f"{base_url}/academic_data?keywords=test&academic_database=Scopus")

    searchdata=searchdata.json()
    found_word = False
    for item in searchdata["articles"]:
        for word in item["title"].split():
            print(word)
            if "test" in word:
                found_word = True
    assert found_word == True
    search_id=searchdata["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")

