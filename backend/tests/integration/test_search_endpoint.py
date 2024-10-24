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

# Initialize TestClient
client = TestClient(app)

from tests.integration.tools.base_url import base_url

session = get_cookie()


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
def test_create_search(db_session):
    """
    Test the search creation API endpoint.
    """
    # Step 1: Create a user for authentication
    user_data = {
        "username": "search_user",
        "password": "testpassword",
        "email": "searchuser@example.com"
    }
    user_response = client.post("/users/create", json=user_data)
    assert user_response.status_code == 201
    created_user_id = user_response.json()["user_id"]

    # Step 2: Authenticate the user to get an access token
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    # Step 3: Use the access token to create a search
    search_data = {
        "user_id": created_user_id,
        "search_keywords": ["test", "example"],
        "title": "Test Search"
    }
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    search_response = client.post("/search/create", json=search_data, headers=headers)
    assert search_response.status_code == 201

    # Step 4: Verify the created search in the database
    created_search_id = search_response.json()["search_id"]
    created_search = db_session.query(Search).filter_by(search_id=created_search_id).first()
    assert created_search is not None
    assert created_search.title == search_data["title"]
    print(f"Created search: {created_search}")
    session.delete(f"{base_url}/search/user/search/title?search_id={created_search_id}")



@pytest.mark.search
def test_get_search_by_id(db_session):
    """
    Test the API endpoint to retrieve a search by its search_id.
    """
    # Step 1: Create a user for authentication
    user_data = {
        "username": "search_user_2",
        "password": "testpassword",
        "email": "searchuser2@example.com"
    }
    user_response = client.post("/users/create", json=user_data)
    assert user_response.status_code == 201
    created_user_id = user_response.json()["user_id"]

    # Step 2: Authenticate the user to get an access token
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    # Step 3: Use the access token to create a search
    search_data = {
        "user_id": created_user_id,
        "search_keywords": ["AI", "machine learning"],
        "title": "AI and ML Search"
    }
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    search_response = client.post("/search/create", json=search_data, headers=headers)
    assert search_response.status_code == 201

    created_search_id = search_response.json()["search_id"]

    # Print the access token and search ID for debugging
    print(f"Access token: {access_token}")
    print(f"Created search ID: {created_search_id}")

    # Step 4: Wait to ensure the transaction has been committed
    time.sleep(5)

    # Step 5: Use the access token to retrieve the search
    get_search_response = client.get(f"/search/searchbyid/{created_search_id}", headers=headers)

    assert get_search_response.status_code == 200

    search = get_search_response.json()
    assert search["search_id"] == created_search_id
    assert search["title"] == search_data["title"]
    print(f"Retrieved search: {search}")
    session.delete(f"{base_url}/search/user/search/title?search_id={created_search_id}")


@pytest.mark.search
def test_get_search_300(db_session):
    """
    Test the API endpoint to retrieve the last 300 searches for a user,
    and verify that additional searches are rejected once the limit is reached.
    """
    # Step 1: Create a user for authentication
    user_data = {
        "username": "test300",
        "password": "testpassword",
        "email": "searchuser2@example.com"
    }
    user_response = client.post("/users/create", json=user_data)
    assert user_response.status_code == 201
    created_user_id = user_response.json()["user_id"]

    # Step 2: Authenticate the user to get an access token
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    list_of_300_search_ids =[]
    # Step 3: Insert 300 searches with the "username-datetimestamp" naming convention
    for i in range(300):
        search_data = {
            "user_id": created_user_id,
            "search_keywords": [f"keyword_{i}"],
            "title": f"test300-{time.strftime('%Y-%m-%d %H:%M:%S')}"
        }
        search_response = client.post("/search/create", json=search_data, headers=headers)
        assert search_response.status_code == 201
        list_of_300_search_ids.append(search_response.json()["search_id"])
        print(f"Inserted search {i + 1}")

    # Step 4: Wait to ensure the transactions have been committed
    time.sleep(5)

    # Step 5: Attempt to create a 301st search, which should be rejected
    extra_search_data = {
        "user_id": created_user_id,
        "search_keywords": ["extra", "search"],
        "title": "test300-extra-search"
    }
    extra_search_response = client.post("/search/create", json=extra_search_data, headers=headers)

    # Step 6: Assert that the 301st search is rejected
    assert extra_search_response.status_code == 400  # Bad Request for exceeding the limit
    assert extra_search_response.json()[
               "detail"] == "Search limit exceeded. Please delete some searches before creating new ones."

    # Step 7: Retrieve the last 300 searches using the cookie for the token
    headers_with_cookie = {
        "Cookie": f"access_token={access_token}"
    }

    search_history_response = client.get("/search/user/searches", headers=headers_with_cookie)

    # Log the response for debugging
    print(f"Response content for /user/searches: {search_history_response.json()}")
    print(f"Response status code: {search_history_response.status_code}")

    # Step 8: Verify the status code and content
    assert search_history_response.status_code == 200
    searches = search_history_response.json()

    # Step 9: Verify there are 300 searches, and at least one of the searches follows the naming convention
    assert isinstance(searches, list)
    assert len(searches) == 300  # Ensure exactly 300 searches are returned

    # Check that the recent searches follow the "username-datetimestamp" convention
    latest_search_title = f"test300-{time.strftime('%Y-%m-%d')}"  # Check for the date prefix
    assert any(search["title"].startswith(latest_search_title) for search in searches)
    print(f"Retrieved {len(searches)} searches")
    for item in list_of_300_search_ids:
        session.delete(f"{base_url}/search/user/search/title?search_id={item}")


@pytest.mark.search
def test_get_search_by_id_not_found(db_session):
    """
    Test the API endpoint to retrieve a search by its search_id when the search is not found.
    """
    # Step 1: Create a user and authenticate them
    user_data = {
        "username": "search_user_3",
        "password": "testpassword",
        "email": "searchuser3@example.com"
    }
    user_response = client.post("/users/create", json=user_data)
    assert user_response.status_code == 201
    created_user_id = user_response.json()["user_id"]

    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    # Step 2: Attempt to get a non-existent search
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    non_existent_search_id = 99999  # Some non-existent ID
    get_search_response = client.get(f"/search/searchbyid/{non_existent_search_id}", headers=headers)

    # Step 3: Ensure a 404 status code is returned
    assert get_search_response.status_code == 404
    assert get_search_response.json() == {"detail": "Search not found"}


@pytest.mark.search
def test_get_search_articles_no_articles(db_session):
    """
    Test the API endpoint to retrieve a search without articles.
    """
    # Step 1: Create a user for authentication
    user_data = {
        "username": "search_user_4",
        "password": "testpassword",
        "email": "searchuser4@example.com"
    }
    user_response = client.post("/users/create", json=user_data)
    assert user_response.status_code == 201
    created_user_id = user_response.json()["user_id"]

    # Step 2: Authenticate the user to get an access token
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Step 3: Create a search without articles
    search_data = {
        "user_id": created_user_id,
        "search_keywords": ["test"],
        "title": "Search Without Articles"
    }
    search_response = client.post("/search/create", json=search_data, headers=headers)
    assert search_response.status_code == 201
    created_search_id = search_response.json()["search_id"]

    # Step 4: Retrieve articles for the search
    headers_with_cookie = {
        "Cookie": f"access_token={access_token}"
    }
    get_articles_response = client.get(f"/search/user/articles?search_id={created_search_id}",
                                       headers=headers_with_cookie)

    # Step 5: Ensure no articles are returned
    assert get_articles_response.status_code == 200
    articles = get_articles_response.json()
    assert isinstance(articles, list)
    assert len(articles) == 0  # No articles associated with the search
    session.delete(f"{base_url}/search/user/search/title?search_id={created_search_id}")


@pytest.mark.search
def test_update_search_title(db_session):
    """
    Test the API endpoint to update the title of a search.
    """
    # Step 1: Create a user for authentication
    user_data = {
        "username": "search_user_5",
        "password": "testpassword",
        "email": "searchuser5@example.com"
    }
    user_response = client.post("/users/create", json=user_data)
    assert user_response.status_code == 201
    created_user_id = user_response.json()["user_id"]

    # Step 2: Authenticate the user to get an access token
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Step 3: Create a search
    search_data = {
        "user_id": created_user_id,
        "search_keywords": ["test"],
        "title": "Old Title"
    }
    search_response = client.post("/search/create", json=search_data, headers=headers)
    assert search_response.status_code == 201
    created_search_id = search_response.json()["search_id"]

    # Step 4: Update the search title
    new_title = "Updated Title"
    update_data = {
        "title": new_title
    }
    headers = {
        "Cookie": f"access_token={access_token}"
    }
    update_response = client.put(f"/search/user/search/title?search_id={created_search_id}", json=update_data,
                                 headers=headers)

    assert update_response.status_code == 200
    updated_search = update_response.json()
    assert updated_search["title"] == new_title
    session.delete(f"{base_url}/search/user/search/title?search_id={created_search_id}")


@pytest.mark.search
def test_expired_token(db_session):
    """
    Test the /search/user/searches endpoint with an expired token.
    """
    # Step 1: Create a user
    user_data = {"username": "user_expired", "password": "password", "email": "user_expired@example.com"}
    user_response = client.post("/users/create", json=user_data)
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
    search_history_response = client.get("/search/user/searches", headers=headers_with_cookie)

    # Step 4: Assert that the response status is 401 Unauthorized
    assert search_history_response.status_code == 401
    assert search_history_response.json() == {"detail": "Token has expired"}


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
    Test the /search/user/searches endpoint with an invalid token.
    """
    # Create an invalid token
    invalid_token = "invalid_token_value"

    # Step 2: Call the endpoint with the invalid token
    headers_with_cookie = {"Cookie": f"access_token={invalid_token}"}
    search_history_response = client.get("/search/user/searches")

    assert search_history_response.status_code == 401





def test_get_valid_token_status_200(db_session):
    """
    Test the /search/user/searches endpoint with an valid cookie returns 200.
    """

    # Step 2: Call the endpoint with the cookie
    search_history_response = session.get(f"{base_url}/search/user/searches")

    assert search_history_response.status_code == 200


def test_get_valid_token_search_user_searches_response_schema(db_session):
    """
    Test the /search/user/searches endpoint with an valid cookie and check response schema

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

    # Step 2: Call the endpoint with the cookie
    search_history_response = session.get(f"{base_url}/search/user/searches")

    assert search_history_response.status_code == 200
    data = search_history_response.json()

    assert isinstance(data[0]["search_id"], int)
    assert isinstance(data[0]["search_keywords"], list)
    assert data[0]["search_keywords"][0] == "test"
    assert isinstance(data[0]["status"], str)
    assert isinstance(data[0]["user_id"], int)
    assert data[0]["search_date"] is None
    search_request = search_request.json()
    search_id = search_request["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


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
    search_id = 1
    apiQuery = "test"
    queryString = "&academic_database=Scopus&academic_database=ScienceDirect"
    #create a new search to query
    search_request = session.get(f"{base_url}/academic_data?keywords={apiQuery}{queryString}")
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
    assert data == []





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
