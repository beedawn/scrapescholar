import pytest
from sqlalchemy.orm import Session
from app.crud.searchkeyword import (
    get_search_keyword,
    get_search_keywords,
    create_search_keyword,
    delete_search_keyword
)

from app.schemas.searchkeyword import SearchKeywordCreate
from app.schemas.search import SearchCreate
from app.schemas.keyword import KeywordCreate
from app.crud.search import create_search, delete_search
from app.crud.keyword import create_keyword, delete_keyword
from app.crud.user import  get_user_by_username
from app.db.session import SessionLocal
from fastapi.exceptions import HTTPException


mock_search_data = {"title": "Test Search", "search_keywords": ["sample"]}
mock_keyword_data = {"keyword": "sample_keyword"}


def generate_unique_search_keyword_data(search_id=1, keyword_id=1):
    return {
        "search_id": search_id,
        "keyword_id": keyword_id
    }


@pytest.fixture
def test_db_session():
    """Fixture to provide a database session with rollback for testing."""
    db = SessionLocal()
    db.begin_nested()
    yield db
    db.rollback()
    db.close()


def create_search_test(created_user, test_db_session):
    search_data_with_user = {**mock_search_data, "user_id": created_user.user_id}
    search_in = SearchCreate(**search_data_with_user)
    created_search = create_search(test_db_session, search_in)
    return created_search


def delete_search_test(search_id, test_db_session):
    delete_search(test_db_session, search_id)
    return None


def create_search_keyword_test(search_keyword_data, test_db_session):
    search_keyword_in = SearchKeywordCreate(**search_keyword_data)
    created_search_keyword = create_search_keyword(test_db_session, search_keyword_in)
    return created_search_keyword


def create_keyword_test(test_db_session):
    keyword_in = KeywordCreate(**mock_keyword_data)
    created_keyword = create_keyword(test_db_session, keyword_in)
    return created_keyword


def delete_keyword_test(keyword_id, test_db_session):
    delete_keyword(test_db_session, keyword_id)
    return None


def setup(test_db_session):
    test_user = get_user_by_username(test_db_session, "testuser")
    created_search = create_search_test(test_user, test_db_session)
    created_keyword = create_keyword_test(test_db_session)
    search_keyword_data = {
        "search_id": created_search.search_id,
        "keyword_id": created_keyword.keyword_id
    }
    return search_keyword_data


def teardown(search_keyword_data, test_db_session, created_search_keyword):
    if created_search_keyword is not None:
        delete_search_keyword(test_db_session, created_search_keyword.search_keyword_id)
    delete_keyword_test(search_keyword_data["keyword_id"], test_db_session)
    delete_search_test(search_keyword_data["search_id"], test_db_session)
    return None


def test_create_search_keyword(test_db_session: Session):
    """Test creating a new search keyword."""
    search_keyword_data = setup(test_db_session)
    created_search_keyword = create_search_keyword_test(search_keyword_data, test_db_session)
    assert created_search_keyword.search_id == search_keyword_data["search_id"]
    assert created_search_keyword.keyword_id == search_keyword_data["keyword_id"]
    teardown(search_keyword_data, test_db_session, created_search_keyword)


def test_get_search_keyword(test_db_session: Session):
    """Test retrieving a search keyword by ID."""
    search_keyword_data = setup(test_db_session)
    created_search_keyword = create_search_keyword_test(search_keyword_data, test_db_session)
    fetched_search_keyword = get_search_keyword(test_db_session, created_search_keyword.search_keyword_id)
    assert fetched_search_keyword.search_keyword_id == created_search_keyword.search_keyword_id
    teardown(search_keyword_data, test_db_session, created_search_keyword)


def test_get_search_keywords(test_db_session: Session):
    """Test retrieving a list of search keywords with pagination."""
    test_user = get_user_by_username(test_db_session, "testuser")

    created_search = create_search_test(test_user, test_db_session)

    created_keyword_1 = create_keyword_test(test_db_session)
    created_keyword_2 = create_keyword_test(test_db_session)
    created_keyword_3 = create_keyword_test(test_db_session)

    search_keyword_data_list = [
        generate_unique_search_keyword_data(search_id=created_search.search_id, keyword_id=created_keyword_1.keyword_id),
        generate_unique_search_keyword_data(search_id=created_search.search_id, keyword_id=created_keyword_2.keyword_id),
        generate_unique_search_keyword_data(search_id=created_search.search_id, keyword_id=created_keyword_3.keyword_id)
    ]
    created_search_keywords = []
    for search_keyword_data in search_keyword_data_list:
        created_search_keyword = create_search_keyword_test(search_keyword_data, test_db_session)
        created_search_keywords.append(created_search_keyword)

    search_keywords = get_search_keywords(test_db_session, skip=0, limit=2)
    assert len(search_keywords) == 2
    for created_search_keyword in created_search_keywords:
        delete_search_keyword(test_db_session, created_search_keyword.search_keyword_id)
    for search_keyword_data in search_keyword_data_list:
        delete_keyword_test(search_keyword_data["keyword_id"], test_db_session)
    delete_search_test(created_search.search_id, test_db_session)


def test_delete_search_keyword(test_db_session: Session):
    """Test deleting a search keyword."""
    search_keyword_data = setup(test_db_session)
    created_search_keyword = create_search_keyword_test(search_keyword_data, test_db_session)

    deleted_search_keyword = delete_search_keyword(test_db_session, created_search_keyword.search_keyword_id)
    assert deleted_search_keyword.search_keyword_id == created_search_keyword.search_keyword_id

    with pytest.raises(HTTPException) as exc_info:
        get_search_keyword(test_db_session, created_search_keyword.search_keyword_id)
    assert exc_info.value.status_code == 404
    teardown(search_keyword_data, test_db_session, None)


def test_get_search_keyword_not_found(test_db_session: Session):
    """Test error handling when a search keyword is not found."""
    with pytest.raises(HTTPException) as exc_info:
        get_search_keyword(test_db_session, search_keyword_id=9999)
    assert exc_info.value.status_code == 404


def test_delete_search_keyword_not_found(test_db_session: Session):
    """Test error handling when trying to delete a non-existent search keyword."""
    with pytest.raises(HTTPException) as exc_info:
        delete_search_keyword(test_db_session, search_keyword_id=9999)
    assert exc_info.value.status_code == 404
