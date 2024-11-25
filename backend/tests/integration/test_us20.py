from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
import pytest
import requests
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url
from app.schemas.user import UserCreate, UserUpdate
from endpoints.auth.auth import login
from app.crud.user import (
    get_user,
    get_user_by_username,
    create_user,
    update_user,
    delete_user,
    verify_password,
    decrypt
)
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_db, SessionLocal
import os
from dotenv import load_dotenv

client = TestClient(app)
session = get_cookie()
load_dotenv()

# Access an environment variable
scopus_api_key = os.getenv('SCOPUS_APIKEY')
sciencedirect_api_key = os.getenv('SCIENCEDIRECT_APIKEY')
scopus_inst_token = os.getenv('SCOPUS_INSTTOKEN')


@pytest.fixture
def test_db_session():
    """Fixture to provide a database session for testing"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



request_body_sciencedirect = {
    "sciencedirect": sciencedirect_api_key,
    "scopus": ""
}

request_body_scopus = {
    "sciencedirect": "",
    "scopus": scopus_api_key
}


#UT-20.2
def test_sciencedirect_custom_apikey(test_db_session):
    response = session.post(f"{base_url}/academic_data?keywords=test&academic_database=ScienceDirect",
                            json=request_body_sciencedirect)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["articles"], list)
    for item in data["articles"]:
        assert "methodology" in item
        assert isinstance(item["methodology"], int)
        assert item["methodology"] >= 0 & item[
            "methodology"] <= 1
        assert "clarity" in item
        assert isinstance(item["clarity"], int)
        assert item["clarity"] >= 0 & item["clarity"] <= 1
        assert "completeness" in item
        assert isinstance(item["completeness"], int)
        assert item["completeness"] >= 0 & item["completeness"] <= 1
        assert "transparency" in item
        assert isinstance(item["transparency"], int)
        assert item["transparency"] >= 0 & item["transparency"] <= 1
    search_id = data["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")

#US-20.2
def test_scopus_custom_apikey(test_db_session):
    response = session.post(f"{base_url}/academic_data?keywords=test&academic_database=Scopus",
                            json=request_body_scopus)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["articles"], list)
    for item in data["articles"]:
        assert "methodology" in item
        assert isinstance(item["methodology"], int)
        assert item["methodology"] >= 0 & item[
            "methodology"] <= 1
        assert "clarity" in item
        assert isinstance(item["clarity"], int)
        assert item["clarity"] >= 0 & item["clarity"] <= 1
        assert "completeness" in item
        assert isinstance(item["completeness"], int)
        assert item["completeness"] >= 0 & item["completeness"] <= 1
        assert "transparency" in item
        assert isinstance(item["transparency"], int)
        assert item["transparency"] >= 0 & item["transparency"] <= 1
    search_id = data["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
