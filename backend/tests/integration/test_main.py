from fastapi import FastAPI

from fastapi.testclient import TestClient

from app.main import app
from app.main import check_response

from fastapi.testclient import TestClient
from tests.integration.tools.get_cookie import get_cookie
from app.main import app
from tests.integration.tools.base_url import base_url


client = TestClient(app)
session = get_cookie()

def test_read_main():
    response = client.get("/health_check")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_check_response():
    class ArticleMock:
        def __init__(self, article_id):
            self.article_id = article_id
    response = check_response([ArticleMock(1)], 1)
    assert response == 2


def test_check_response_no_id():
    class ArticleMock:
        def __init__(self, article_id):
            self.article_id = article_id
    response = check_response([], 1)
    assert response == 1





def test_read_main():
    response = client.get("/health_check")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_sciencedirect_present_in_sources():
    response = session.get(f"{base_url}/academic_sources")
    assert response.status_code == 200
    data = response.json()
    assert "ScienceDirect" in data


def test_scopus_present_in_sources():
    response = session.get(f"{base_url}/academic_sources")
    assert response.status_code == 200
    data = response.json()
    assert "Scopus" in data

