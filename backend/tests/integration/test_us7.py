import pytest
from fastapi.testclient import TestClient
from app.main import app
import requests
from app.db.session import get_db, SessionLocal
from endpoints.auth.auth import login
from fastapi.security import OAuth2PasswordRequestForm
from tests.integration.tools.delete_user import delete_user
from app.crud.searchshare import delete_search_share
from app.models import SearchShare
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url
from tests.integration.tools.blankAPIKey import request_body
client = TestClient(app)
session = get_cookie()


@pytest.fixture
def test_db_session():
    """Fixture to provide a database session with rollback for testing."""
    db = SessionLocal()
    db.begin_nested()

    yield db

    db.rollback()
    db.close()


user_data = {
    "username": "testuser_2",
    "password": "testpassword",
    "email": "testuser2@example.com"
}


def get_cookie_2():
    session = requests.Session()
    db = next(get_db())
    login_credentials = OAuth2PasswordRequestForm(
        username=user_data["username"],
        password=user_data["password"],
    )
    login_response = login(data=login_credentials)

    cookie = login_response.headers.get('set-cookie')

    cookie_separated = cookie.split(';')
    for section in cookie_separated:
        if section.startswith('access_token='):
            token_value = section.split('=')[1]
    session.cookies.set('access_token', token_value)
    return session


#UT-7.2
def test_sharing_works_between_users(test_db_session):
    response = session.post(f"{base_url}/users/create", json=user_data)
    assert response.status_code == 201

    created_user_id = response.json()["user_id"]

    searchdata = session.post(f"{base_url}/academic_data?keywords=test&academic_database=Scopus", json=request_body)
    searchdata = searchdata.json()
    search_id = searchdata["search_id"]

    searchdata = session.put(f"{base_url}/search/share?search_id={search_id}&share_user={user_data['email']}")
    assert searchdata.status_code == 200
    share_id = searchdata.json()["share_id"]

    added_share = test_db_session.query(SearchShare).filter(SearchShare.share_id == share_id).all()
    assert len(added_share) == 1

    session2 = get_cookie_2()

    searchdata = session2.get(f"{base_url}/search/user/articles?search_id={search_id}")
    assert searchdata.status_code == 200

    delete_search_share(test_db_session, share_id)
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
    delete_user(created_user_id, session, base_url)


#UT-7.3

def test_401_when_not_shared(test_db_session):
    response = session.post(f"{base_url}/users/create", json=user_data)

    assert response.status_code == 201

    created_user_id = response.json()["user_id"]

    searchdata = session.post(f"{base_url}/academic_data?keywords=test&academic_database=Scopus", json=request_body)
    searchdata = searchdata.json()
    search_id = searchdata["search_id"]

    session2 = get_cookie_2()

    searchdata = session2.get(f"{base_url}/search/user/articles?search_id={search_id}")
    assert searchdata.status_code == 401

    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
    delete_user(created_user_id, session, base_url)
