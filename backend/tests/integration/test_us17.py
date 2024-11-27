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

client = TestClient(app)
session = get_cookie()


@pytest.fixture
def test_db_session():
    """Fixture to provide a database session for testing"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


mock_user_data = {
    "username": "user",
    "email": "user@example.com",
    "password": "testpassword",
    "role_id": 2
}


def get_cookie_2():
    session = requests.Session()
    db = next(get_db())
    login_credentials = OAuth2PasswordRequestForm(
        username=mock_user_data["username"],
        password=mock_user_data["password"],
    )
    login_response = login(data=login_credentials)

    cookie = login_response.headers.get('set-cookie')

    cookie_separated = cookie.split(';')
    for section in cookie_separated:
        if section.startswith('access_token='):
            token_value = section.split('=')[1]
    session.cookies.set('access_token', token_value)
    return session

#UT-17.3
def test_user_put(test_db_session):
    user_in = UserCreate(**mock_user_data)
    created_user = create_user(test_db_session, user_in)
    nonadmin_session = get_cookie_2()
    put_request = {
      "username": mock_user_data["username"],
      "email": mock_user_data["email"],
      "user_id": created_user.user_id,
      "role_id": 1,
      "registration_date": "2024-11-07T20:39:36.586Z"
    }
    response = nonadmin_session.put(f"{base_url}/users/update/{created_user.user_id}", json=put_request)
    assert response.status_code == 401

    delete_user(test_db_session, created_user.user_id)



def test_user_delete(test_db_session):
    user_in = UserCreate(**mock_user_data)
    created_user = create_user(test_db_session, user_in)
    nonadmin_session = get_cookie_2()
    response = nonadmin_session.delete(f"{base_url}/users/delete/{created_user.user_id}")
    assert response.status_code == 401

    delete_user(test_db_session, created_user.user_id)
