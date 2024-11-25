from fastapi.testclient import TestClient
from app.main import app
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url
from tests.integration.tools.blankAPIKey import request_body

session = get_cookie()
client = TestClient(app)


#UT-5.2
def test_user_data_slash_update_put():
    searchdata = session.post(f"{base_url}/academic_data?keywords=test&academic_database=Scopus", json=request_body)
    searchdata = searchdata.json()
    article_id = searchdata["articles"][0]["article_id"]
    search_id = searchdata["search_id"]
    data = {
        "article_id": article_id,
        "relevancy_color": "Not Relevant"
    }
    session.put(f"{base_url}/user_data/update", json=data)

    response = session.get(f"{base_url}/search/user/articles?search_id={search_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        if item["article_id"] == article_id:
            assert item["color"] == "Not Relevant"
    search_id = searchdata["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
