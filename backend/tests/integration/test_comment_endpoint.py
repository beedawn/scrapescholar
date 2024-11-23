from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db, SessionLocal

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

mock_comment_data = {
    "comment_text": "This is a test comment"
}


def test_create_comment():
    search_id = create_search()

    mock_article_data_dynamic = mock_article_data.copy()
    mock_article_data_dynamic["search_id"] = search_id

    response = session.post(f"{base_url}/article/", json=mock_article_data_dynamic)
    assert response.status_code == 201
    article_id = response.json()["article_id"]

    response = session.post(f"{base_url}/comment/article/{article_id}", json=mock_comment_data)
    assert response.status_code == 201
    assert response.json()["comment_text"] == mock_comment_data["comment_text"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_get_comments():
    search_id = create_search()

    mock_article_data_dynamic = mock_article_data.copy()
    mock_article_data_dynamic["search_id"] = search_id
    response = session.post(f"{base_url}/article/", json=mock_article_data_dynamic)
    article_id = response.json()["article_id"]

    session.post(f"{base_url}/comment/article/{article_id}", json=mock_comment_data)

    response = session.get(f"{base_url}/comment/article/{article_id}/comments")
    assert response.status_code == 200
    assert len(response.json()) > 0
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_update_comment():
    search_id = create_search()

    mock_article_data_dynamic = mock_article_data.copy()
    mock_article_data_dynamic["search_id"] = search_id
    response = session.post(f"{base_url}/article/", json=mock_article_data_dynamic)
    article_id = response.json()["article_id"]

    comment_response = session.post(f"{base_url}/comment/article/{article_id}", json=mock_comment_data)
    comment_id = comment_response.json()["comment_id"]

    updated_comment = {"comment_text": "Updated comment text"}
    response = session.put(f"{base_url}/comment/{comment_id}", json=updated_comment)
    assert response.status_code == 200
    assert response.json()["comment_text"] == updated_comment["comment_text"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_delete_comment():
    search_id = create_search()

    mock_article_data_dynamic = mock_article_data.copy()
    mock_article_data_dynamic["search_id"] = search_id
    response = session.post(f"{base_url}/article/", json=mock_article_data_dynamic)
    article_id = response.json()["article_id"]

    comment_response = session.post(f"{base_url}/comment/article/{article_id}", json=mock_comment_data)
    comment_id = comment_response.json()["comment_id"]

    response = session.delete(f"{base_url}/comment/{comment_id}")
    assert response.status_code == 204
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
