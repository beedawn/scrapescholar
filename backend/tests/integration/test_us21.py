
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.crud.user import get_user_by_username
from app.main import app
from app.db.session import SessionLocal
from app.crud.search import create_search, delete_search, get_search
from app.schemas.search import SearchCreate
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url
from endpoints.search.search import post_search_no_route


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

#UT-21.2
def test_deny_after_300_searches_exist(test_db_session):
    i=0
    test_user = get_user_by_username(test_db_session, "testuser")
    list_of_searches =[]
    while i < 301:
        new_search=SearchCreate(user_id=test_user.user_id, title= str(i))
        list_of_searches.append(new_search)
        i +=1
    created_searches = []
    for item in list_of_searches:
        created_search=create_search(test_db_session, item)
        created_searches.append(created_search)
    #try a new search, should not go well
    api_query = "test"
    query_string = "&academic_database=Scopus&academic_database=ScienceDirect"
    search_request = session.get(f"{base_url}/academic_data?keywords={api_query}{query_string}")
    assert search_request.status_code == 507
    search_response = search_request.json()
    assert search_response["message"] == "Insufficient storage, you have 300 saved searches. Please delete some to continue"
    for item in created_searches:
        delete_search(test_db_session, item.search_id)

#UT-21.3
def test_search_delete_endpoint(test_db_session):
    test_user = get_user_by_username(test_db_session, "testuser")
    new_search=SearchCreate(user_id=test_user.user_id, title= "Test search")
    created_search=create_search(test_db_session, new_search)
    search_request = session.delete(f"{base_url}/search/user/search/title?search_id={created_search.search_id}")
    assert search_request.status_code == 200
    try:
        search = get_search(test_db_session, created_search.search_id)
    except HTTPException as err:
        search = None
    assert search is None

