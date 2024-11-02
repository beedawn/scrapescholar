# backend/tests/database/test_crud_searchshare.py

import pytest
from sqlalchemy.orm import Session
from app.crud.searchshare import (
    get_search_share,
    get_search_shares,
    create_search_share,
    delete_search_share
)
from app.schemas.searchshare import SearchShareCreate
from app.models.searchshare import SearchShare
from app.db.session import SessionLocal
from fastapi.exceptions import HTTPException
from datetime import datetime

# Mock data for SearchShare creation with unique data generator
def generate_unique_share_data(search_id=1, shared_with_user_id=2, shared_by_user_id=1):
    return {
        "search_id": search_id,
        "shared_with_user_id": shared_with_user_id,
        "shared_by_user_id": shared_by_user_id,
        "share_date": datetime.utcnow()
    }

@pytest.fixture
def test_db_session():
    """Fixture to provide a database session with rollback for testing."""
    db = SessionLocal()
    db.begin_nested()

    yield db

    db.rollback()
    db.close()

def test_create_search_share(test_db_session: Session):
    """Test creating a new search share."""
    #need to have two users and a search to share a search

    search_share_data = generate_unique_share_data()
    search_share_in = SearchShareCreate(**search_share_data)
    created_search_share = create_search_share(test_db_session, search_share_in)

    # Verifying the fields in the created search share
    assert created_search_share.search_id == search_share_data["search_id"]
    assert created_search_share.shared_with_user_id == search_share_data["shared_with_user_id"]
    assert created_search_share.shared_by_user_id == search_share_data["shared_by_user_id"]

def test_get_search_share(test_db_session: Session):
    """Test retrieving a search share by ID."""
    search_share_data = generate_unique_share_data()
    search_share_in = SearchShareCreate(**search_share_data)
    created_search_share = create_search_share(test_db_session, search_share_in)

    # Retrieve the search share
    fetched_search_share = get_search_share(test_db_session, created_search_share.share_id)
    assert fetched_search_share.share_id == created_search_share.share_id

def test_get_search_shares(test_db_session: Session):
    """Test retrieving a list of search shares with pagination."""
    # Create a few search shares for pagination test
    search_share_data_list = [
        generate_unique_share_data(search_id=1, shared_with_user_id=2, shared_by_user_id=1),
        generate_unique_share_data(search_id=2, shared_with_user_id=3, shared_by_user_id=1),
        generate_unique_share_data(search_id=3, shared_with_user_id=4, shared_by_user_id=1)
    ]

    for search_share_data in search_share_data_list:
        search_share_in = SearchShareCreate(**search_share_data)
        create_search_share(test_db_session, search_share_in)

    # Retrieve paginated search shares
    search_shares = get_search_shares(test_db_session, skip=0, limit=2)
    assert len(search_shares) == 2

def test_delete_search_share(test_db_session: Session):
    """Test deleting a search share."""
    search_share_data = generate_unique_share_data()
    search_share_in = SearchShareCreate(**search_share_data)
    created_search_share = create_search_share(test_db_session, search_share_in)

    # Delete the search share
    deleted_search_share = delete_search_share(test_db_session, created_search_share.share_id)
    assert deleted_search_share.share_id == created_search_share.share_id

    # Verify search share no longer exists
    with pytest.raises(HTTPException) as exc_info:
        get_search_share(test_db_session, created_search_share.share_id)
    assert exc_info.value.status_code == 404

def test_get_search_share_not_found(test_db_session: Session):
    """Test error handling when a search share is not found."""
    with pytest.raises(HTTPException) as exc_info:
        get_search_share(test_db_session, share_id=9999)
    assert exc_info.value.status_code == 404

def test_delete_search_share_not_found(test_db_session: Session):
    """Test error handling when trying to delete a non-existent search share."""
    with pytest.raises(HTTPException) as exc_info:
        delete_search_share(test_db_session, share_id=9999)
    assert exc_info.value.status_code == 404
