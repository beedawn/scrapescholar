import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.db.session import get_db, SessionLocal
from app.schemas.comment import CommentCreate
from app.models.comment import Comment

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

# Mock comment data
mock_comment_data = {
    "user_id": 1,
    "comment_text": "This is a test comment"
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
    "search_id": 1,
    "user_id": 1
}

def test_create_comment():
    # First, create an article to attach the comment
    response = client.post("/articles/", json=mock_article_data)
    article_id = response.json()["article_id"]

    # Add a comment to the article
    response = client.post(f"/comment/article/{article_id}", json=mock_comment_data)
    assert response.status_code == 201
    assert response.json()["comment_text"] == mock_comment_data["comment_text"]

def test_get_comments():
    # Create an article and a comment
    response = client.post("/articles/", json=mock_article_data)
    article_id = response.json()["article_id"]
    client.post(f"/comment/article/{article_id}", json=mock_comment_data)

    # Get comments for the article
    response = client.get(f"/comment/article/{article_id}/comments")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_comment():
    # Create an article and a comment
    response = client.post("/articles/", json=mock_article_data)
    article_id = response.json()["article_id"]
    comment_response = client.post(f"/comment/article/{article_id}", json=mock_comment_data)
    comment_id = comment_response.json()["comment_id"]

    # Update the comment
    updated_comment = {"comment_text": "Updated comment text"}
    response = client.put(f"/comment/{comment_id}", json=updated_comment)
    assert response.status_code == 200
    assert response.json()["comment_text"] == updated_comment["comment_text"]

def test_delete_comment():
    # Create an article and a comment
    response = client.post("/articles/", json=mock_article_data)
    article_id = response.json()["article_id"]
    comment_response = client.post(f"/comment/article/{article_id}", json=mock_comment_data)
    comment_id = comment_response.json()["comment_id"]

    # Delete the comment
    response = client.delete(f"/comment/{comment_id}")
    assert response.status_code == 204