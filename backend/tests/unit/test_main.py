from fastapi import FastAPI

from fastapi.testclient import TestClient
from tests.integration.tools.get_cookie import get_cookie
from app.main import app

client = TestClient(app)
session = get_cookie()

def test_read_main():
    response = client.get("/health_check")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_sciencedirect_present_in_sources():
    response = session.get("/academic_sources")
    assert response.status_code == 200
    data = response.json()
    assert "ScienceDirect" in data

def test_scopus_present_in_sources():
    response = session.get("/academic_sources")
    assert response.status_code == 200
    data = response.json()
    assert "Scopus" in data
    