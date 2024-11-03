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
from app.crud.search import create_search, delete_search
from app.db.session import SessionLocal
from fastapi.exceptions import HTTPException
from datetime import datetime
from app.crud.user import create_user, get_user_by_username, delete_user
from tests.database.test_crud_searchkeyword import create_search_test
from app.schemas.user import UserCreate


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


#TODO:
#wrangle these tests
#missing setup items required for each test


def setup(test_db_session):
    new_user_init = UserCreate(username="test_user2", password="test_user2")
    test_user = get_user_by_username(test_db_session, "testuser")
    created_search = create_search_test(test_user, test_db_session)
    new_user = create_user(test_db_session, new_user_init)
    return created_search, test_user, new_user


def teardown(test_db_session, created_search_share, new_user):
    delete_search_share(test_db_session, created_search_share.share_id)
    delete_search(test_db_session, created_search_share.search_id)
    delete_user(test_db_session, new_user.user_id)

    return None


def test_create_search_share(test_db_session: Session):
    """Test creating a new search share."""
    #need to have two users and a search to share a search
    new_search, test_user, new_user = setup(test_db_session)

    search_share_data = generate_unique_share_data(new_search.search_id, test_user.user_id, new_user.user_id)

    search_share_in = SearchShareCreate(**search_share_data)
    created_search_share = create_search_share(test_db_session, search_share_in)

    # Verifying the fields in the created search share
    assert created_search_share.search_id == search_share_data["search_id"]
    assert created_search_share.shared_with_user_id == search_share_data["shared_with_user_id"]
    assert created_search_share.shared_by_user_id == search_share_data["shared_by_user_id"]
    teardown(test_db_session, created_search_share, new_user)


def test_get_search_share(test_db_session: Session):
    """Test retrieving a search share by ID."""
    new_search, test_user, new_user = setup(test_db_session)

    search_share_data = generate_unique_share_data(new_search.search_id, test_user.user_id, new_user.user_id)
    search_share_in = SearchShareCreate(**search_share_data)
    created_search_share = create_search_share(test_db_session, search_share_in)

    # Retrieve the search share
    fetched_search_share = get_search_share(test_db_session, created_search_share.share_id)
    assert fetched_search_share.share_id == created_search_share.share_id
    delete_search_share(test_db_session, created_search_share.share_id)
    delete_search(test_db_session, new_search.search_id)
    delete_user(test_db_session, new_user.user_id)

def test_get_search_shares(test_db_session: Session):
    """Test retrieving a list of search shares with pagination."""
    new_search, test_user, new_user = setup(test_db_session)
    new_search_2 = create_search_test(test_user, test_db_session)
    new_search_3 = create_search_test(test_user, test_db_session)
    searches = [new_search, new_search_2, new_search_3]
    # Create a few search shares for pagination test
    search_share_data_list = [
        generate_unique_share_data(search_id=new_search.search_id, shared_with_user_id=new_user.user_id, shared_by_user_id=test_user.user_id),
        generate_unique_share_data(search_id=new_search_2.search_id, shared_with_user_id=new_user.user_id, shared_by_user_id=test_user.user_id),
        generate_unique_share_data(search_id=new_search_3.search_id, shared_with_user_id=new_user.user_id, shared_by_user_id=test_user.user_id)
    ]
    shares = []
    for search_share_data in search_share_data_list:
        search_share_in = SearchShareCreate(**search_share_data)
        new_share= create_search_share(test_db_session, search_share_in)
        shares.append(new_share)

    # Retrieve paginated search shares
    search_shares = get_search_shares(test_db_session, skip=0, limit=2)
    assert len(search_shares) == 2
    for share in shares:
        delete_search_share(test_db_session, share.share_id)
    for search in searches:
        delete_search(test_db_session, search.search_id)
    delete_user(test_db_session, new_user.user_id)



def test_delete_search_share(test_db_session: Session):
    """Test deleting a search share."""

    new_search, test_user, new_user = setup(test_db_session)

    search_share_data = generate_unique_share_data(new_search.search_id, test_user.user_id, new_user.user_id)
    search_share_in = SearchShareCreate(**search_share_data)
    created_search_share = create_search_share(test_db_session, search_share_in)

    # Delete the search share
    deleted_search_share = delete_search_share(test_db_session, created_search_share.share_id)
    assert deleted_search_share.share_id == created_search_share.share_id

    # Verify search share no longer exists
    with pytest.raises(HTTPException) as exc_info:
        get_search_share(test_db_session, created_search_share.share_id)
    assert exc_info.value.status_code == 404
    delete_user(test_db_session, new_user.user_id)
    delete_search(test_db_session, new_search.search_id)


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
