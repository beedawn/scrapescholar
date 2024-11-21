# tests/integration/test_article_endpoint.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db, SessionLocal
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url
from tests.integration.tools.create_search import create_search

session = get_cookie()
client = TestClient(app)

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
    "search_id": 1
}



def test_create_article():

    # Step 5: Create a search and get the search ID
    search_id = create_search()

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

    response = session.post(f"{base_url}/article", json=mock_article_data)
    assert response.status_code == 201
    print("TITLE")
    print(response.json())
    assert response.json()["title"] == mock_article_data["title"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_get_article():


    # First, create a search and get the search ID
    # Step 5: Create a search and get the search ID
    search_id = create_search()

    # Create the article with dynamic search_id and user_id
    mock_article_data_dynamic = mock_article_data.copy()
    mock_article_data_dynamic["search_id"] = search_id

    # First, create the article
    response = session.post(f"{base_url}/article/", json=mock_article_data_dynamic)
    assert response.status_code == 201
    article_id = response.json()["article_id"]

    # Fetch the article by ID
    response = session.get(f"{base_url}/article/{article_id}")
    assert response.status_code == 200
    assert response.json()["title"] == mock_article_data_dynamic["title"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_delete_article():


    # First, create a search and get the search ID
    # Step 5: Create a search and get the search ID
    search_id = create_search()

    # Create the article with dynamic search_id and user_id
    mock_article_data_dynamic = mock_article_data.copy()
    mock_article_data_dynamic["search_id"] = search_id

    # First, create the article
    response = session.post(f"{base_url}/article/", json=mock_article_data_dynamic)
    assert response.status_code == 201
    article_id = response.json()["article_id"]

    # Delete the article
    response = session.delete(f"{base_url}/article/{article_id}")
    assert response.status_code == 204
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_update_article():

    # First, create a search and get the search ID
    # Step 5: Create a search and get the search ID
    search_id = create_search()

    # Create the article with dynamic search_id and user_id
    mock_article_data_dynamic = mock_article_data.copy()
    mock_article_data_dynamic["search_id"] = search_id

    # First, create the article
    response = session.post(f"{base_url}/article/", json=mock_article_data_dynamic)
    assert response.status_code == 201
    article_id = response.json()["article_id"]

    # Update the article
    updated_data = {"title": "Updated Test Article"}
    response = session.put(f"{base_url}/article/{article_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Article"
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")

