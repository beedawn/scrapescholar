# tests/integration/test_comment_endpoint.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db, SessionLocal
from app.schemas.comment import CommentCreate
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.create_search import create_search
from tests.integration.tools.base_url import base_url


client = TestClient(app)
session = get_cookie()


def override_get_db():
    db = SessionLocal()
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
    "search_id": 1  # This will be updated dynamically
}

# Mock comment data
mock_comment_data = {
    "comment_text": "This is a test comment"
}


def test_create_comment():
    # Create a search first and get the search_id
    search_id = create_search()

    # Update the mock_article_data with the dynamic search_id
    mock_article_data_dynamic = mock_article_data.copy()
    mock_article_data_dynamic["search_id"] = search_id

    # Create the article
    response = session.post(f"{base_url}/article/", json=mock_article_data_dynamic)
    assert response.status_code == 201
    article_id = response.json()["article_id"]

    # Add a comment to the article
    response = session.post(f"{base_url}/comment/article/{article_id}", json=mock_comment_data)
    assert response.status_code == 201
    assert response.json()["comment_text"] == mock_comment_data["comment_text"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_get_comments():
    # Create a search first and get the search_id
    search_id = create_search()

    # Create an article and add a comment
    mock_article_data_dynamic = mock_article_data.copy()
    mock_article_data_dynamic["search_id"] = search_id
    response = session.post(f"{base_url}/article/", json=mock_article_data_dynamic)
    article_id = response.json()["article_id"]

    # Add a comment
    session.post(f"{base_url}/comment/article/{article_id}", json=mock_comment_data)

    # Get comments for the article
    response = session.get(f"{base_url}/comment/article/{article_id}/comments")
    assert response.status_code == 200
    assert len(response.json()) > 0
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_update_comment():
    # Create a search first and get the search_id
    search_id = create_search()

    # Create an article and a comment
    mock_article_data_dynamic = mock_article_data.copy()
    mock_article_data_dynamic["search_id"] = search_id
    response = session.post(f"{base_url}/article/", json=mock_article_data_dynamic)
    article_id = response.json()["article_id"]

    # Add a comment
    comment_response = session.post(f"{base_url}/comment/article/{article_id}", json=mock_comment_data)
    comment_id = comment_response.json()["comment_id"]

    # Update the comment
    updated_comment = {"comment_text": "Updated comment text"}
    response = session.put(f"{base_url}/comment/{comment_id}", json=updated_comment)
    assert response.status_code == 200
    assert response.json()["comment_text"] == updated_comment["comment_text"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_delete_comment():
    # Create a search first and get the search_id
    search_id = create_search()
    # Create an article and a comment
    mock_article_data_dynamic = mock_article_data.copy()
    mock_article_data_dynamic["search_id"] = search_id
    response = session.post(f"{base_url}/article/", json=mock_article_data_dynamic)
    article_id = response.json()["article_id"]

    # Add a comment
    comment_response = session.post(f"{base_url}/comment/article/{article_id}", json=mock_comment_data)
    comment_id = comment_response.json()["comment_id"]

    # Delete the comment
    response = session.delete(f"{base_url}/comment/{comment_id}")
    assert response.status_code == 204
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
