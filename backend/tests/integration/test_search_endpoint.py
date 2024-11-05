# tests/unit/test_search_endpoint.py
import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app
from app.models.search import Search
from app.models.article import Article
from app.db.session import SessionLocal
import os
import time
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
import jwt
from datetime import datetime, timedelta
from tests.integration.tools.get_cookie import get_cookie
from app.models.user import User
from types import SimpleNamespace
from tests.integration.tools.delete_user import delete_user
# Initialize TestClient
client = TestClient(app)

from tests.integration.tools.base_url import base_url

session = get_cookie()

from endpoints.search.search import post_search_no_route


@pytest.fixture(scope="function")
def db_session():
    """Provides a transactional scope around a series of operations."""
    db = SessionLocal()  # Assuming SessionLocal is defined in your app to connect to the database
    try:
        yield db
    finally:
        # Try to truncate the search table, but ignore errors if the table doesn't exist
        try:
            db.execute(text("TRUNCATE TABLE \"Search\" RESTART IDENTITY CASCADE;"))
            db.commit()
        except ProgrammingError as e:
            if "UndefinedTable" in str(e):
                print(f"Warning: {e}. The 'search' table does not exist.")
            else:
                raise  # re-raise if it's not an UndefinedTable error
        finally:
            db.close()


# ----------------------- SEARCH ENDPOINT TEST SUITE -----------------------

@pytest.mark.search
def test_expired_token(db_session):
    """
    Test the /search/user/searches endpoint with an expired token.
    """
    # Step 1: Create a user
    user_data = {"username": "user_expired", "password": "password", "email": "user_expired@example.com"}
    user_response = session.post(f"{base_url}/users/create", json=user_data)
    assert user_response.status_code == 201
    created_user_id = user_response.json()["user_id"]

    # Step 2: Generate an expired token
    secret_key = os.getenv("SECRET_KEY")  # Fetch the SECRET key from your environment or config
    expired_token = jwt.encode({
        "sub": str(created_user_id),
        "exp": datetime.utcnow() - timedelta(seconds=1)  # Set expiration in the past
    }, secret_key, algorithm="HS256")

    # Step 3: Call the endpoint with the expired token
    headers_with_cookie = {"Cookie": f"access_token={expired_token}"}
    search_history_response = client.get(f"{base_url}/search/user/searches", headers=headers_with_cookie)

    # Step 4: Assert that the response status is 401 Unauthorized
    assert search_history_response.status_code == 401
    assert search_history_response.json() == {"detail": "Token has expired"}
    delete_user(created_user_id, session, base_url)


@pytest.mark.search
def test_get_invalid_token(db_session):
    """
    Test the /search/user/searches endpoint with an invalid token.
    """
    # Create an invalid token
    invalid_token = "invalid_token_value"

    # Step 2: Call the endpoint with the invalid token
    headers_with_cookie = {"Cookie": f"access_token={invalid_token}"}
    search_history_response = client.get("/search/user/searches", headers=headers_with_cookie)

    assert search_history_response.status_code == 401
    assert search_history_response.json() == {"detail": "Invalid token"}


def test_get_no_token(db_session):
    """
    Test the /search/user/searches endpoint no token.
    """
    # Create an invalid token
    invalid_token = "invalid_token_value"

    # Step 2: Call the endpoint with the invalid token
    search_history_response = client.get("/search/user/searches")

    assert search_history_response.status_code == 401


def test_get_valid_token_status_200(db_session):
    """
    Test the /search/user/searches endpoint with an valid cookie returns 200.
    """

    # Step 2: Call the endpoint with the cookie
    search_history_response = session.get(f"{base_url}/search/user/searches")

    assert search_history_response.status_code == 200


def test_get_valid_token_academic_data_response_schema(db_session):
    """
    Test the /academic_data endpoint with a valid cookie and check response schema, 
    as well as verify that the search results are saved to the database (UT-4.7).

    response should look like:

    [
    {
        "search_id": 1,
        "search_keywords": [
            "test"
        ],
        "status": "active",
        "user_id": 1,
        "search_date": null,
        "title": "testuser-2024-10-05 07:34:54.766305"
    }
    ]
    """

    apiQuery = "test"
    queryString = "&academic_database=Scopus&academic_database=ScienceDirect"
    #create a new search to query
    search_request = session.get(f"{base_url}/academic_data?keywords={apiQuery}{queryString}")

    """
    article looks like
    "id": 0,
                "title": "Impact of cardiac rehabilitation exercise frequency on exercise capacity in patients with coronary artery disease: a retrospective study",
                "date": "2024-12-31",
                "citedby": "0",
                "link": "https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85204941817&origin=inward",
                "abstract": "",
                "document_type": "Article",
                "source": "Scopus",
                
                "color": "red",
                "relevance_score": 29,
                "methodology": 0,
                "clarity": 0,
                "completeness": 0,
                "transparency": 0
    """
    assert search_request.status_code == 200
    data = search_request.json()
    assert isinstance(data["search_id"], int)
    assert isinstance(data["articles"], list)
    assert isinstance(data["articles"][0]["title"], str)
    assert isinstance(data["articles"][0]["date"], str)
    assert isinstance(data["articles"][0]["citedby"], (str, int))
    assert isinstance(data["articles"][0]["link"], str)
    assert isinstance(data["articles"][0]["date"], str)
    assert isinstance(data["articles"][0]["abstract"], str)
    assert isinstance(data["articles"][0]["document_type"], str)
    assert isinstance(data["articles"][0]["source"], str)

    assert isinstance(data["articles"][0]["color"], str)
    assert isinstance(data["articles"][0]["relevance_score"], float)
    assert isinstance(data["articles"][0]["methodology"], int)
    assert isinstance(data["articles"][0]["clarity"], int)
    assert isinstance(data["articles"][0]["completeness"], int)
    assert isinstance(data["articles"][0]["transparency"], int)

    # Step 5: Verify that the search and its results were saved to the database
    search_id = data["search_id"]
    article_id = data["articles"][0]["article_id"]
    saved_search = db_session.query(Search).filter_by(search_id=search_id).first()

    # Ensure the search was saved
    assert saved_search is not None
    assert saved_search.search_keywords == apiQuery.split(", ")

    # Ensure the articles associated with the search were saved to the database
    saved_articles = db_session.query(Article).filter(Article.article_id == article_id).all()
    assert len(saved_articles) > 0  # Ensure articles were saved

    # Check attributes of the first article in the database
    saved_article = saved_articles[0]
    assert saved_article.title == data["articles"][0]["title"]
    assert saved_article.link == data["articles"][0]["link"]
    assert saved_article.search_id == search_id

    search_id = data["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_get_valid_token_past_search_response_schema(db_session):
    """
    Test the /academic_data endpoint with an valid cookie and check response schema

    response should look like, a list of articles:

    [
 {
        "abstract": "",
        "search_id": 1,
        "user_id": 1,
        "link": "https://www.sciencedirect.com/science/article/pii/S0092867423013193?dgcid=api_sd_search-api-endpoint",
        "title": "XIST directly regulates X-linked and autosomal genes in naive human pluripotent cells",
        "relevance_score": 66.0,

        "citedby": null,
        "document_type": null,
        "article_id": 30,
        "date": "2024-01-04",
        "doi": null,
        "source_id": 1
    },
]
    """
    api_query = "test"
    query_string = "&academic_database=Scopus&academic_database=ScienceDirect"
    #create a new search to query
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
    # assert isinstance(data[0]["citedby"], str)
    assert isinstance(data[0]["link"], str)
    assert isinstance(data[0]["date"], str)
    assert isinstance(data[0]["abstract"], str)
    # assert isinstance(data[0]["document_type"], str)
    # assert isinstance(data[0]["source"], str)
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

    response should look like:

{
    "title": "testuser-2024-10-05 08:06:57.273926",
    "keywords": [
        "test"
    ]
}
    """
    search_id = 1
    apiQuery = "test"
    queryString = "&academic_database=Scopus&academic_database=ScienceDirect"
    #create a new search to query
    search_request = session.get(f"{base_url}/academic_data?keywords={apiQuery}{queryString}")
    title = session.get(f"{base_url}/search/user/search/title?search_id={search_id}")

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

    response should look like:

{
    "search_id": 1,
    "search_keywords": [
        "x"
    ],
    "status": "active",
    "user_id": 1,
    "search_date": null,
    "title": "new one"
}
    """
    search_id = 1
    body = {"title": "new test title"}
    apiQuery = "test"
    queryString = "&academic_database=Scopus&academic_database=ScienceDirect"
    #create a new search to query
    search_request = session.get(f"{base_url}/academic_data?keywords={apiQuery}{queryString}")
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
    search_request = search_request.json()
    search_id = search_request["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_delete_valid_token_search_title_response_schema(db_session):
    """
    Test the /search/user/search/title endpoint with an valid cookie and check response schema

    response should look like:

{
    "search_id": 1,
    "search_keywords": [
        "x"
    ],
    "status": "active",
    "user_id": 1,
    "search_date": null,
    "title": "new one"
}
    """

    apiQuery = "test"
    queryString = "&academic_database=Scopus&academic_database=ScienceDirect"
    #create a new search to query
    search_request = session.get(f"{base_url}/academic_data?keywords={apiQuery}{queryString}")
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
def test_get_searches_empty_result(db_session):
    """
    Test the /user/searches endpoint for a user with no searches in the database.
    """

    search_history_response = session.get(f"{base_url}/search/user/searches")

    assert search_history_response.status_code == 200
    assert search_history_response.json() == []


@pytest.mark.search
def test_get_searches_non_empty_result(db_session):
    """
    Test the /user/searches endpoint for a user with one or more searches in the database.
    """

    apiQuery = "test"
    queryString = "&academic_database=Scopus&academic_database=ScienceDirect"
    #create a new search to query
    search_request = session.get(f"{base_url}/academic_data?keywords={apiQuery}{queryString}")
    # Step 4: Call the endpoint with a valid token

    search_history_response = session.get(f"{base_url}/search/user/searches")

    # Step 5: Assert that the response contains search data
    assert search_history_response.status_code == 200
    data = search_history_response.json()

    assert isinstance(data, list)
    assert len(data) > 0  # Confirm that at least one search result is returned
    assert "search_id" in data[0]
    search_request_json = search_request.json()
    search_id = search_request_json["search_id"]
    delete = session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
