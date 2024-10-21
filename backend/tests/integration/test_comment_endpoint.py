# tests/integration/test_comment_endpoint.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db, SessionLocal
from app.schemas.comment import CommentCreate

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
    "username": "testuser_5",
    "password": "testpassword",
    "email": "testuser_5@example.com"
}

# Mock login data
mock_login_data = {
    "username": "testuser_5",
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

# Mock comment data
mock_comment_data = {
    "comment_text": "This is a test comment"
}

# Helper function to register a new user and get auth token
def create_and_authenticate_user():
    # Step 1: Register a new user
    response = client.post("/users/create", json=mock_user_data)
    assert response.status_code == 201
    
    # Step 2: Login to get the token
    login_response = client.post("/auth/login", data={"username": mock_login_data["username"], "password": mock_login_data["password"]})

    assert login_response.status_code == 200
    return login_response.json()["access_token"]

def test_create_comment():
    token = create_and_authenticate_user()
    assert token is not None, "Authentication token was not generated."
    
    response = client.post("/article/", json=mock_article_data, headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 201, f"Expected status 201, got {response.status_code}"

    article_id = response.json()["article_id"]

    # Add a comment to the article
    response = client.post(f"/comment/article/{article_id}", json=mock_comment_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["comment_text"] == mock_comment_data["comment_text"]

def test_get_comments():
    token = create_and_authenticate_user()

    # Create an article and a comment
    response = client.post("/article/", json=mock_article_data, headers={"Authorization": f"Bearer {token}"})
    article_id = response.json()["article_id"]
    client.post(f"/comment/article/{article_id}", json=mock_comment_data, headers={"Authorization": f"Bearer {token}"})

    # Get comments for the article
    response = client.get(f"/comment/article/{article_id}/comments", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_comment():
    token = create_and_authenticate_user()

    # Create an article and a comment
    response = client.post("/article/", json=mock_article_data, headers={"Authorization": f"Bearer {token}"})
    article_id = response.json()["article_id"]
    comment_response = client.post(f"/comment/article/{article_id}", json=mock_comment_data, headers={"Authorization": f"Bearer {token}"})
    comment_id = comment_response.json()["comment_id"]

    # Update the comment
    updated_comment = {"comment_text": "Updated comment text"}
    response = client.put(f"/comment/{comment_id}", json=updated_comment, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["comment_text"] == updated_comment["comment_text"]

def test_delete_comment():
    token = create_and_authenticate_user()

    # Create an article and a comment
    response = client.post("/article/", json=mock_article_data, headers={"Authorization": f"Bearer {token}"})
    article_id = response.json()["article_id"]
    comment_response = client.post(f"/comment/article/{article_id}", json=mock_comment_data, headers={"Authorization": f"Bearer {token}"})
    comment_id = comment_response.json()["comment_id"]

    # Delete the comment
    response = client.delete(f"/comment/{comment_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204