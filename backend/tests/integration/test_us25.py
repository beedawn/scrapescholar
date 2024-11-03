from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url

session = get_cookie()


#UT-5.2
def test_relevancy_score():
    searchdata = session.get(f"{base_url}/academic_data?keywords=test&academic_database=Scopus")
    assert searchdata.status_code == 200

    searchdata = searchdata.json()

    for item in searchdata["articles"]:
        assert isinstance(item["relevance_score"], float)
    search_id = searchdata["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


#ut-25.3
def test_user_data_slash_update_put():
    data = {
        "article_id": 1,
        "relevancy_color": "Not Relevant"
    }
    searchdata = session.get(f"{base_url}/academic_data?keywords=test&academic_database=Scopus")
    searchdata = searchdata.json()
    search_id = searchdata["search_id"]
    article_relevance_score = searchdata["articles"][0]["relevance_score"]
    response = session.get(f"{base_url}/search/user/articles?search_id={search_id}")
    assert response.status_code == 200
    data = response.json()
    new_relevance_score = data[0]["relevance_score"]
    assert article_relevance_score == new_relevance_score


    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
