from fastapi.testclient import TestClient
from app.main import app
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url

session = get_cookie()
client = TestClient(app)


#UT-23.1
def test_user_data_slash_update_put_valid_body():
    searchdata = session.get(f"{base_url}/academic_data?keywords=test&academic_database=Scopus")
    searchdata = searchdata.json()
    article = searchdata['articles'][0]
    data = {
        "article_id": article['article_id'],
        "relevancy_color": "Not Relevant",
        "evaluation_criteria": "Pending",
        "methodology": "0",
        "clarity": "0",
        "transparency": "1",
        "completeness": "1"
    }
    putrequest = session.put(f"{base_url}/user_data/update", json=data)
    response = session.get(f"{base_url}/search/user/articles?search_id={searchdata['search_id']}")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    for item in data:
        if item["article_id"] == article['article_id']:
            assert item["color"] == "Not Relevant"
            assert item["evaluation_criteria"] == "Pending"
            assert item["methodology"] == 0
            assert item["clarity"] == 0
            assert item["transparency"] == 1
            assert item["completeness"] == 1

    putrequest = putrequest.json()
    assert putrequest['user_id'] == 1
    assert isinstance(putrequest['article_id'], int)
    assert putrequest['article_id'] == article['article_id']
    assert putrequest['relevancy_color'] == 'Not Relevant'
    assert putrequest['evaluation_criteria'] == 'Pending'
    assert putrequest['methodology'] == 0
    assert putrequest['clarity'] == 0
    assert putrequest['transparency'] == 1
    assert putrequest['completeness'] == 1

    search_id = searchdata["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


#UT-23.2
def test_user_data_slash_update_put_no_cookie():
    searchdata = session.get(f"{base_url}/academic_data?keywords=test&academic_database=Scopus")
    data = {
        "article_id": 1,
        "relevancy_color": "Not Relevant",
        "evaluation_criteria": "Pending",
        "methodology": "0",
        "clarity": "0",
        "transparency": "1",
        "completeness": "1"
    }
    putrequest = client.put(f"{base_url}/user_data/update", json=data)
    assert putrequest.status_code == 401
    data = putrequest.json()

    assert data["detail"] == "Invalid token"
    search_id = searchdata.json()["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


#UT-23.3     
def test_user_data_slash_update_put_invalid_body():
    searchdata = session.get(f"{base_url}/academic_data?keywords=test&academic_database=Scopus")
    data = {
        "relevancy_color": "Not Relevant",
    }
    putrequest = session.put(f"{base_url}/user_data/update", json=data)
    assert putrequest.status_code == 422
    data = putrequest.json()

    assert isinstance(data["detail"], list)
    assert data["detail"][0]["type"] == "missing"
    assert isinstance(data["detail"][0]["loc"], list)
    assert data["detail"][0]["loc"][0] == "body"
    assert data["detail"][0]["loc"][1] == "article_id"
    assert data["detail"][0]["msg"] == "Field required"
    assert data["detail"][0]["input"]["relevancy_color"] == "Not Relevant"
    search_id = searchdata.json()["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


# UT-23.4
def test_user_data_slash_update_put_invalid_token_nonexistent_user():
    data = {
        "article_id": 1,
        "relevancy_color": "Not Relevant",
        "evaluation_criteria": "Pending",
        "methodology": "0",
        "clarity": "0",
        "transparency": "1",
        "completeness": "1"
    }

    putrequest = session.put(f"{base_url}/user_data/update", json=data)

    assert putrequest.status_code == 404
    assert putrequest.json() == {"detail": "Userdata not found in put, user not valid in db"}
