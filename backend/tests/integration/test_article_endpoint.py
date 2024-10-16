# tests/integration/test_article_endpoint.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db, SessionLocal

# Test client
client = TestClient(app)

# Override the dependency for testing
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Mock login data for authentication
mock_login_data = {
    "username": "bv_tester",
    "password": "test_password"
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

# Helper function to get an authentication token
def get_auth_token():
    response = client.post("/auth/login", data=mock_login_data)
    assert response.status_code == 200
    return response.json()["access_token"]

def test_create_article():
    token = get_auth_token()

    # Create an article with authentication
    response = client.post("/article/", json=mock_article_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code