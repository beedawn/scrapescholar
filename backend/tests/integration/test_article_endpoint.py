import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app  # Assuming the main app is instantiated in main.py
from app.db.session import get_db
from app.schemas.article import ArticleCreate
from app.models.article import Article

# Test client
client = TestClient(app)

# Override the dependency for testing
def override_get_db():
    db = SessionLocal()  # Assuming you have SessionLocal for the testing DB session
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

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
    "search_id": 1,
    "user_id": 1
}

def test_create_article():
    response = client.post("/article/", json=mock_article_data)
    assert response.status_code == 200
    assert response.json()["title"] == mock_article_data["title"]

def test_get_article():
    # First, create the article
    response = client.post("/article/", json=mock_article_data)
    article_id = response.json()["article_id"]
    
    # Fetch the article by ID
    response = client.get(f"/article/{article_id}")
    assert response.status_code == 200
    assert response.json()["title"] == mock_article_data["title"]

def test_delete_article():
    # First, create the article
    response = client.post("/article/", json=mock_article_data)
    article_id = response.json()["article_id"]

    # Delete the article
    response = client.delete(f"/article/{article_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Article deleted successfully"

def test_get_deleted_article():
    # Try to fetch the deleted article
    response = client.get("/article/9999")  # Assuming 9999 is a non-existent ID
    assert response.status_code == 404
    assert response.json()["detail"] == "Article not found"
