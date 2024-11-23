import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.search import Search
from app.models.article import Article
from app.db.session import SessionLocal
import os
import jwt
from datetime import datetime, timedelta
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.delete_user import delete_user
from tests.integration.tools.base_url import base_url

client = TestClient(app)

session = get_cookie()


@pytest.fixture(scope="function")
def db_session():
    """Provides a transactional scope around a series of operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@pytest.mark.search
def test_expired_token(db_session):
    """
    Test the /search/user/searches endpoint with an expired token.
    """
    user_data = {"username": "user_expired", "password": "password", "email": "user_expired@example.com"}
    user_response = session.post(f"{base_url}/users/create", json=user_data)
    assert user_response.status_code == 201
    created_user_id = user_response.json()["user_id"]

    secret_key = os.getenv("SECRET_KEY")
    expired_token = jwt.encode({
        "sub": str(created_user_id),
        "exp": datetime.utcnow() - timedelta(seconds=1)  # Set expiration in the past
    }, secret_key, algorithm="HS256")

    headers_with_cookie = {"Cookie": f"access_token={expired_token}"}
    search_history_response = client.get(f"{base_url}/search/user/searches", headers=headers_with_cookie)

    assert search_history_response.status_code == 401
    assert search_history_response.json() == {"detail": "Token has expired"}
    delete_user(created_user_id, session, base_url)


@pytest.mark.search
def test_get_invalid_token(db_session):
    """
    Test the /search/user/searches endpoint with an invalid token.
    """
    invalid_token = "invalid_token_value"

    headers_with_cookie = {"Cookie": f"access_token={invalid_token}"}
    search_history_response = client.get("/search/user/searches", headers=headers_with_cookie)

    assert search_history_response.status_code == 401
    assert search_history_response.json() == {"detail": "Invalid token"}


def test_get_no_token(db_session):
    """
    Test the /search/user/searches endpoint no token.
    """
    search_history_response = client.get("/search/user/searches")

    assert search_history_response.status_code == 401


def test_get_valid_token_status_200(db_session):
    """
    Test the /search/user/searches endpoint with an valid cookie returns 200.
    """
    search_history_response = session.get(f"{base_url}/search/user/searches")

    assert search_history_response.status_code == 200


def test_get_valid_token_academic_data_response_schema(db_session):
    """
    Test the /academic_data endpoint with a valid cookie and check response schema, 
    as well as verify that the search results are saved to the database (UT-4.7).
    """

    apiQuery = "test"
    queryString = "&academic_database=Scopus&academic_database=ScienceDirect"

    search_request = session.get(f"{base_url}/academic_data?keywords={apiQuery}{queryString}")
    assert search_request.status_code == 200
    data = search_request.json()
    assert isinstance(data["search_id"], int)
    assert isinstance(data["articles"], list)
    assert isinstance(data["articles"][0]["title"], str)
    assert isinstance(data["articles"][0]["date"], str)
    assert isinstance(data["articles"][0]["citedby"], (str, int))
    assert isinstance(data["articles"][0]["link"], str)
    assert isinstance(data["articles"][0]["date"], str)
    assert isinstance(data["articles"][0]["abstract"], str | None)
    assert isinstance(data["articles"][0]["document_type"], str)
    assert isinstance(data["articles"][0]["source"], str)

    assert isinstance(data["articles"][0]["color"], str)
    assert isinstance(data["articles"][0]["relevance_score"], float)
    assert isinstance(data["articles"][0]["methodology"], int)
    assert isinstance(data["articles"][0]["clarity"], int)
    assert isinstance(data["articles"][0]["completeness"], int)
    assert isinstance(data["articles"][0]["transparency"], int)

    search_id = data["search_id"]
    article_id = data["articles"][0]["article_id"]
    saved_search = db_session.query(Search).filter_by(search_id=search_id).first()

    assert saved_search is not None
    assert saved_search.search_keywords == apiQuery.split(", ")

    saved_articles = db_session.query(Article).filter(Article.article_id == article_id).all()
    assert len(saved_articles) > 0  # Ensure articles were saved

    saved_article = saved_articles[0]
    assert saved_article.title == data["articles"][0]["title"]
    assert saved_article.link == data["articles"][0]["link"]
    assert saved_article.search_id == search_id

    search_id = data["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_get_valid_token_past_search_response_schema(db_session):
    """
    Test the /academic_data endpoint with an valid cookie and check response schema
    """
    api_query = "test"
    query_string = "&academic_database=Scopus&academic_database=ScienceDirect"

    search_request = session.get(f"{base_url}/academic_data?keywords={api_query}{query_string}")
    search_request_data = search_request.json()
    search_id = search_request_data["search_id"]
    past_search = session.get(f"{base_url}/search/user/articles?search_id={search_id}")

    assert search_request.status_code == 200
    assert past_search.status_code == 200
    data = past_search.json()

    assert isinstance(data, list)
    assert isinstance(data[0]["title"], str)
    assert isinstance(data[0]["date"], str)
    assert isinstance(data[0]["link"], str)
    assert isinstance(data[0]["date"], str)
    assert isinstance(data[0]["abstract"], str | None)
    assert isinstance(data[0]["relevance_score"], float)
    search_request = search_request.json()
    search_id = search_request["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_get_valid_token_past_search_bad_search_id(db_session):
    """
    Test the /academic_data endpoint with an valid cookie and bad search id
    """
    search_id = 907848397
    past_search = session.get(f"{base_url}/search/user/articles?search_id={search_id}")
    data = past_search.json()
    assert data == {'detail': 'Search not found'}


def test_get_valid_token_search_title_response_schema(db_session):
    """
    Test the /search/user/search/title endpoint with an valid cookie and check response schema
    """

    apiQuery = "test"
    queryString = "&academic_database=Scopus&academic_database=ScienceDirect"

    search_request = session.get(f"{base_url}/academic_data?keywords={apiQuery}{queryString}")
    search_request_data = search_request.json()
    title = session.get(f"{base_url}/search/user/search/title?search_id={search_request_data['search_id']}")

    assert search_request.status_code == 200
    assert title.status_code == 200
    data = title.json()
    assert isinstance(data["title"], str)
    assert isinstance(data["keywords"], list)
    search_request = search_request.json()
    search_id = search_request["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_put_valid_token_search_title_response_schema(db_session):
    """
    Test the /search/user/search/title endpoint with an valid cookie and check response schema
    """

    body = {"title": "new test title"}
    api_query = "test"
    querystring = "&academic_database=Scopus&academic_database=ScienceDirect"

    search_request = session.get(f"{base_url}/academic_data?keywords={api_query}{querystring}")
    search_request_data = search_request.json()
    search_id = search_request_data['search_id']
    new_title = session.put(f"{base_url}/search/user/search/title?search_id={search_id}", json=body)

    assert search_request.status_code == 200
    assert new_title.status_code == 200
    data = new_title.json()
    assert isinstance(data["search_id"], int)
    assert isinstance(data["search_keywords"], list)
    assert isinstance(data["user_id"], int)
    assert data["search_date"] is None
    assert isinstance(data["title"], str)
    assert data["title"] == "new test title"

    title = session.get(f"{base_url}/search/user/search/title?search_id={search_id}")
    data = title.json()
    assert data["title"] == "new test title"
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_delete_valid_token_search_title_response_schema(db_session):
    """
    Test the /search/user/search/title endpoint with an valid cookie and check response schema
    """

    api_query = "test"
    querystring = "&academic_database=Scopus&academic_database=ScienceDirect"
    search_request = session.get(f"{base_url}/academic_data?keywords={api_query}{querystring}")
    search_request_json = search_request.json()
    search_id = search_request_json["search_id"]
    delete = session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
    articles = db_session.query(Article).filter_by(search_id=search_id).first()
    search = db_session.query(Search).filter_by(search_id=search_id).first()

    assert search_request.status_code == 200
    assert delete.status_code == 200
    data = delete.json()
    assert isinstance(data, list)
    assert len(data) is 0
    assert articles is None
    assert search is None


@pytest.mark.search
def test_get_searches_non_empty_result(db_session):
    """
    Test the /user/searches endpoint for a user with one or more searches in the database.
    """

    api_query = "test"
    querystring = "&academic_database=Scopus&academic_database=ScienceDirect"

    search_request = session.get(f"{base_url}/academic_data?keywords={api_query}{querystring}")
    search_history_response = session.get(f"{base_url}/search/user/searches")

    assert search_history_response.status_code == 200
    data = search_history_response.json()

    assert isinstance(data, list)
    assert len(data) > 0  # Confirm that at least one search result is returned
    assert "search_id" in data[0]
    search_request_json = search_request.json()
    search_id = search_request_json["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
