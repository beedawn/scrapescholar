# backend/tests/database/test_crud_search.py

import pytest
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from app.crud.search import get_search, get_searches, create_search, update_search, delete_search
from app.models.search import Search
from app.schemas.search import SearchCreate, SearchUpdate
from app.db.session import SessionLocal

# Mock data for search creation
mock_search_data = {
    "user_id": 1,
    "search_date": "2024-10-31T12:00:00",
    "search_keywords": ["test", "search"],
    "status": "active",
    "title": "Test Search"
}

@pytest.fixture
def test_db_session():
    """Fixture to provide a database session with rollback for testing."""
    db = SessionLocal()
    db.begin_nested()

    yield db

    db.rollback()
    db.close()

def test_create_search(test_db_session: Session):
    """Test creating a new search entry."""
    search_in = SearchCreate(**mock_search_data)
    created_search = create_search(test_db_session, search_in)
    assert created_search.title == mock_search_data["title"]
    assert created_search.user_id == mock_search_data["user_id"]
    assert created_search.status == mock_search_data["status"]

def test_get_search(test_db_session: Session):
    """Test retrieving a search by ID."""
    search_in = SearchCreate(**mock_search_data)
    created_search = create_search(test_db_session, search_in)
    fetched_search = get_search(test_db_session, created_search.search_id)
    assert fetched_search.search_id == created_search.search_id
    assert fetched_search.title == created_search.title

def test_get_search_not_found(test_db_session: Session):
    """Test handling of retrieving a non-existent search."""
    with pytest.raises(HTTPException) as exc_info:
        get_search(test_db_session, search_id=9999)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Search not found"

def test_get_searches(test_db_session: Session):
    """Test retrieving a list of searches with pagination."""
    # Creating multiple searches
    search_data_list = [
        SearchCreate(**mock_search_data),
        SearchCreate(**{**mock_search_data, "title": "Test Search 2"})
    ]
    for search_data in search_data_list:
        create_search(test_db_session, search_data)

    searches = get_searches(test_db_session, skip=0, limit=2)
    assert len(searches) == 2  # Expected number of retrieved searches

def test_update_search(test_db_session: Session):
    """Test updating a search entry."""
    search_in = SearchCreate(**mock_search_data)
    created_search = create_search(test_db_session, search_in)

    # Update the search entry
    update_data = SearchUpdate(title="Updated Search Title", status="completed")
    updated_search = update_search(test_db_session, created_search.search_id, update_data)
    
    assert updated_search.title == "Updated Search Title"
    assert updated_search.status == "completed"

def test_update_search_not_found(test_db_session: Session):
    """Test updating a non-existent search."""
    update_data = SearchUpdate(title="Updated Search Title")
    with pytest.raises(HTTPException) as exc_info:
        update_search(test_db_session, search_id=9999, search=update_data)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Search not found"

def test_delete_search(test_db_session: Session):
    """Test deleting a search entry."""
    search_in = SearchCreate(**mock_search_data)
    created_search = create_search(test_db_session, search_in)
    
    deleted_search = delete_search(test_db_session, created_search.search_id)
    assert deleted_search.search_id == created_search.search_id

    # Verify search no longer exists
    with pytest.raises(HTTPException) as exc_info:
        get_search(test_db_session, created_search.search_id)
    assert exc_info.value.status_code == 404

def test_delete_search_not_found(test_db_session: Session):
    """Test deleting a non-existent search."""
    with pytest.raises(HTTPException) as exc_info:
        delete_search(test_db_session, search_id=9999)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Search not found"