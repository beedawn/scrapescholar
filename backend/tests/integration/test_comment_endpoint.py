import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app  # Assuming the main app is instantiated in main.py
from app.db.session import get_db
from app.schemas.comment import CommentCreate
from app.models.comment import Comment

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

# Mock comment data
mock_comment_data = {
    "comment_text": "This is a test comment",
    "user_id": 1,
}

def test_create_comment():
    # First, create an article to attach the comment
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
    response = client.post("/article/", json=mock_article_data)
    article_id = response.json()["article_id"]

    # Add a comment to the article
    response = client.post(f"/articles/{article_id}/comments", json=mock_comment_data)
    assert response.status_code == 200
    assert response.json()["comment_text"] == mock_comment_data["comment_text"]

def test_get_comments():
    # Create an article and a comment
    response = client.post("/article/", json=mock_article_data)
    article_id = response.json()["article_id"]
    client.post(f"/articles/{article_id}/comments", json=mock_comment_data)

    # Get comments for the article
    response = client.get(f"/articles/{article_id}/comments")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_comment():
    # Create an article and a comment
    response = client.post("/article/", json=mock_article_data)
    article_id = response.json()["article_id"]
    comment_response = client.post(f"/articles/{article_id}/comments", json=mock_comment_data)
    comment_id = comment_response.json()["comment_id"]

    # Update the comment
    updated_comment = {"comment_text": "Updated comment text"}
    response = client.put(f"/comments/{comment_id}", json=updated_comment)
    assert response.status_code == 200
    assert response.json()["comment_text"] == updated_comment["comment_text"]

def test_delete_comment():
    # Create an article and a comment
    response = client.post("/article/", json=mock_article_data)
    article_id = response.json()["article_id"]
    comment_response = client.post(f"/articles/{article_id}/comments", json=mock_comment_data)
    comment_id = comment_response.json()["comment_id"]

    # Delete the comment
    response = client.delete(f"/comments/{comment_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Comment deleted successfully"