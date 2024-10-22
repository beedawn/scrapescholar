# tests/integration/test_article_endpoint.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db, SessionLocal

client = TestClient(app)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Mock user registration data
mock_user_data = {
    "username": "article_tester",
    "password": "testpassword",
    "email": "article_tester@example.com"
}

# Mock login data
mock_login_data = {
    "username": "article_tester",
    "password": "testpassword"
}

# Mock article data
mock_article_data = {
    "title": "Test Article",
    "date": "2024-10-11",
    "link": "http://example.com/test_article",
    "relevance_score": 95,
    "evaluation_criteria": "High",
    "abstract": "This is a test article.",
    "citedby": 100,
    "document_type": "Journal",
    "source_id": 1,
    "search_id": 1
}

# Helper function to create a search
def create_search(token, user_id):
    # Step 3: Create a search and pass user_id dynamically
    search_data = {
        "user_id": user_id,  # Use dynamic user_id
        "title": "Test Search",
        "search_keywords": ["test", "article"],
        "status": "active"
    }
    response = client.post("/search/create", json=search_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    search_id = response.json()["search_id"]  # Get search_id from response
    return search_id

# Helper function to register and authenticate a user
def create_and_authenticate_user():
    # Step 1: Create a user and get the user ID
    user_data = {
        "username": "testuser_dynamic",
        "password": "testpassword",
        "email": "testuser_dynamic@example.com"
    }
    user_response = client.post("/users/create", json=user_data)
    assert user_response.status_code == 201
    user_id = user_response.json()["user_id"]

    # Step 2: Authenticate the user and get the access token
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    return token, user_id

def test_create_article():
    # Step 4: Get authenticated token and user ID
    token, user_id = create_and_authenticate_user()

    # Step 5: Create a search and get the search ID
    search_id = create_search(token, user_id)

    # Step 6: Create an article with dynamic search_id and user_id
    mock_article_data = {
        "title": "Test Article",
        "date": "2024-10-11",
        "link": "http://example.com/test_article",
        "relevance_score": 95,
        "evaluation_criteria": "High",
        "abstract": "This is a test article.",
        "citedby": 100,
        "document_type": "Journal",
        "source_id": 1,
        "search_id": search_id  # Use dynamic search_id
    }

    response = client.post("/article/", json=mock_article_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["title"] == mock_article_data["title"]

def test_get_article():
    token, user_id = create_and_authenticate_user()

    # First, create a search and get the search ID
    search_id = create_search(token, user_id)

    # Create the article with dynamic search_id and user_id
    mock_article_data_dynamic = mock_article_data.copy()
    mock_article_data_dynamic["search_id"] = search_id

    # First, create the article
    response = client.post("/article/", json=mock_article_data_dynamic, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    article_id = response.json()["article_id"]

    # Fetch the article by ID
    response = client.get(f"/article/{article_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == mock_article_data_dynamic["title"]

def test_delete_article():
    token, user_id = create_and_authenticate_user()  

    # First, create a search and get the search ID
    search_id = create_search(token, user_id)

    # Create the article with dynamic search_id and user_id
    mock_article_data_dynamic = mock_article_data.copy()
    mock_article_data_dynamic["search_id"] = search_id

    # First, create the article
    response = client.post("/article/", json=mock_article_data_dynamic, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    article_id = response.json()["article_id"]

    # Delete the article
    response = client.delete(f"/article/{article_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

def test_update_article():
    token, user_id = create_and_authenticate_user()

    # First, create a search and get the search ID
    search_id = create_search(token, user_id)

    # Create the article with dynamic search_id and user_id
    mock_article_data_dynamic = mock_article_data.copy()
    mock_article_data_dynamic["search_id"] = search_id

    # First, create the article
    response = client.post("/article/", json=mock_article_data_dynamic, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    article_id = response.json()["article_id"]

    # Update the article
    updated_data = {"title": "Updated Test Article"}
    response = client.put(f"/article/{article_id}", json=updated_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Article"
