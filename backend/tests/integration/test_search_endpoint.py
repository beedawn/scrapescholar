# tests/unit/test_search_endpoint.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app  # Import the FastAPI app
from app.models.user import User
from app.models.search import Search
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from app.db.session import SessionLocal
import os
import time
import random
import string

# Initialize TestClient
client = TestClient(app)

# Password hashing context
hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture(scope="module")
def db_session():
    """Provides a transactional scope around a series of operations."""
    db = SessionLocal()  # Assuming SessionLocal is defined in your app to connect to the database
    try:
        yield db
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

@pytest.mark.search
def test_get_search_300(db_session):
    """
    Test the API endpoint to retrieve the last 300 searches for a user.
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

    # Step 3: Insert 300 random searches
    for i in range(300):
        search_data = {
            "user_id": created_user_id,
            "search_keywords": [f"keyword_{i}", random.choice(["Cybersecurity", "Non Profit", "Community", "Social"])],
            "title": f"Search Title {i} - {''.join(random.choices(string.ascii_letters, k=5))}"
        }
        search_response = client.post("/search/create", json=search_data, headers=headers)
        assert search_response.status_code == 201
        print(f"Inserted search {i+1}")

    # Step 4: Wait to ensure the transactions have been committed
    time.sleep(5)

    # Step 5: Retrieve the last 300 searches using the cookie for the token
    headers_with_cookie = {
        "Cookie": f"access_token={access_token}"
    }

    search_history_response = client.get("/search/user/searches", headers=headers_with_cookie)

    # Log the response for debugging
    print(f"Response content for /user/searches: {search_history_response.json()}")
    print(f"Response status code: {search_history_response.status_code}")

    # Step 6: Verify the status code and content
    assert search_history_response.status_code == 200
    searches = search_history_response.json()
    
    # Step 7: Verify there are 300 searches, and at least one of the searches is in the list
    assert isinstance(searches, list)
    assert len(searches) == 300  # Ensure exactly 300 searches are returned
    
    # Check that at least one of the recent searches is in the list
    latest_search_title = f"Search Title 299"  # The last inserted search
    assert any(search["title"].startswith(latest_search_title) for search in searches)
    print(f"Retrieved {len(searches)} searches")

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