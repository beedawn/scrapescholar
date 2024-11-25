import pytest
from fastapi.security import OAuth2PasswordRequestForm

from endpoints.download.download import csv_generator, build_fieldnames, add_user_comments_to_list
from sqlalchemy.orm import Session

from academic_databases.SearchResult import SearchResult
from io import StringIO
from tests.integration.tools.create_search import create_search
import csv
import pytest
import requests
from app.main import app
from app.db.session import get_db, SessionLocal
from endpoints.auth.auth import login
import pytest
from fastapi.testclient import TestClient
from tests.integration.tools.delete_user import delete_user
from app.crud.searchshare import delete_search_share
from app.models import SearchShare
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url
from tests.integration.tools.blankAPIKey import request_body

client = TestClient(app)
session = get_cookie()

user_data = {
    "username": "testuser_22",
    "password": "testpassword",
    "email": "testuser22@example.com"
}


def get_cookie_2():
    session = requests.Session()
    db = next(get_db())
    login_credentials = OAuth2PasswordRequestForm(
        username=user_data["username"],
        password=user_data["password"],
    )
    login_response = login(login_credentials, db)

    cookie = login_response.headers.get('set-cookie')

    cookie_separated = cookie.split(';')
    for section in cookie_separated:
        if section.startswith('access_token='):
            token_value = section.split('=')[1]
    session.cookies.set('access_token', token_value)
    return session


@pytest.fixture
def test_db_session():
    """Fixture to provide a database session for testing"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# UT-8.3
def test_csv_filename_in_response(test_db_session):
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

    response = session2.get(f"{base_url}/download?search_id={search_id}")
    content_disposition = response.headers["Content-Disposition"]
    response = session2.get(f"{base_url}/search/user/search/title?search_id={search_id}")
    response = response.json()
    title = response["title"]
    assert f'attachment; filename={title}' in content_disposition
    delete_search_share(test_db_session, share_id)
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
    delete_user(created_user_id, session, base_url)
