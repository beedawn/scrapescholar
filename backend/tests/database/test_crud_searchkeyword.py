# backend/tests/database/test_crud_searchkeyword.py

import pytest
from sqlalchemy.orm import Session
from app.crud.searchkeyword import (
    get_search_keyword,
    get_search_keywords,
    create_search_keyword,
    delete_search_keyword
)
from app.schemas.searchkeyword import SearchKeywordCreate
from app.db.session import SessionLocal
from app.models.searchkeyword import SearchKeyword
from fastapi.exceptions import HTTPException

# Mock data for SearchKeyword creation
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

def test_create_search_keyword(test_db_session: Session):
    """Test creating a new search keyword."""
    search_keyword_data = generate_unique_search_keyword_data()
    search_keyword_in = SearchKeywordCreate(**search_keyword_data)
    created_search_keyword = create_search_keyword(test_db_session, search_keyword_in)

    # Verifying the fields in the created search keyword
    assert created_search_keyword.search_id == search_keyword_data["search_id"]
    assert created_search_keyword.keyword_id == search_keyword_data["keyword_id"]

def test_get_search_keyword(test_db_session: Session):
    """Test retrieving a search keyword by ID."""
    search_keyword_data = generate_unique_search_keyword_data()
    search_keyword_in = SearchKeywordCreate(**search_keyword_data)
    created_search_keyword = create_search_keyword(test_db_session, search_keyword_in)

    # Retrieve the search keyword
    fetched_search_keyword = get_search_keyword(test_db_session, created_search_keyword.search_keyword_id)
    assert fetched_search_keyword.search_keyword_id == created_search_keyword.search_keyword_id

def test_get_search_keywords(test_db_session: Session):
    """Test retrieving a list of search keywords with pagination."""
    # Create a few search keywords for pagination test
    search_keyword_data_list = [
        generate_unique_search_keyword_data(search_id=1, keyword_id=1),
        generate_unique_search_keyword_data(search_id=2, keyword_id=2),
        generate_unique_search_keyword_data(search_id=3, keyword_id=3)
    ]

    for search_keyword_data in search_keyword_data_list:
        search_keyword_in = SearchKeywordCreate(**search_keyword_data)
        create_search_keyword(test_db_session, search_keyword_in)

    # Retrieve paginated search keywords
    search_keywords = get_search_keywords(test_db_session, skip=0, limit=2)
    assert len(search_keywords) == 2

def test_delete_search_keyword(test_db_session: Session):
    """Test deleting a search keyword."""
    search_keyword_data = generate_unique_search_keyword_data()
    search_keyword_in = SearchKeywordCreate(**search_keyword_data)
    created_search_keyword = create_search_keyword(test_db_session, search_keyword_in)

    # Delete the search keyword
    deleted_search_keyword = delete_search_keyword(test_db_session, created_search_keyword.search_keyword_id)
    assert deleted_search_keyword.search_keyword_id == created_search_keyword.search_keyword_id

    # Verify search keyword no longer exists
    with pytest.raises(HTTPException) as exc_info:
        get_search_keyword(test_db_session, created_search_keyword.search_keyword_id)
    assert exc_info.value.status_code == 404

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
