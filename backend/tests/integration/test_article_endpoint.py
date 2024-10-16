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

# Helper function to register and authenticate a user
def create_and_authenticate_user():
    # Step 1: Register a new user
    response = client.post("/users/create", json=mock_user_data)
    assert response.status_code == 201

    # Step 2: Login to get the token
    login_response = client.post("/auth/login", data=mock_login_data)
    assert login_response.status_code == 200
    return login_response.json()["access_token"]

def test_create_article():
    token = create_and_authenticate_user()

    # Create an article with authentication
    response = client.post("/article/", json=mock_article_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["title"] == mock_article_data["title"]

def test_get_article():
    token = create_and_authenticate_user()

    # First, create the article
    response = client.post("/article/", json=mock_article_data, headers={"Authorization": f"Bearer {token}"})
    article_id = response.json()["article_id"]

    # Fetch the article by ID
    response = client.get(f"/article/{article_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == mock_article_data["title"]

def test_delete_article():
    token = create_and_authenticate_user()

    # First, create the article
    response = client.post("/article/", json=mock_article_data, headers={"Authorization": f"Bearer {token}"})
    article_id = response.json()["article_id"]

    # Delete the article
    response = client.delete(f"/article/{article_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

def test_get_deleted_article():
    token = create_and_authenticate_user()

    # Try to fetch the deleted article
    response = client.get("/article/9999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Article not found"

def test_update_article():
    token = create_and_authenticate_user()

    # First, create the article
    response = client.post("/article/", json=mock_article_data, headers={"Authorization": f"Bearer {token}"})
    article_id = response.json()["article_id"]

    # Update the article
    updated_data = {"title": "Updated Test Article"}
    response = client.put(f"/article/{article_id}", json=updated_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Article"