import pytest
from sqlalchemy.orm import Session
from app.crud.keyword import (
    get_keyword,
    get_keywords,
    create_keyword,
    update_keyword,
    delete_keyword
)
from app.schemas.keyword import KeywordCreate, KeywordUpdate
from app.db.session import SessionLocal
from fastapi.exceptions import HTTPException


@pytest.fixture
def test_db_session():
    """Fixture to provide a database session for testing."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


mock_keyword_data = {
    "keyword": "example_keyword"
}


def test_create_keyword(test_db_session: Session):
    """Test creating a new keyword."""
    keyword_in = KeywordCreate(**mock_keyword_data)
    created_keyword = create_keyword(test_db_session, keyword_in)

    assert created_keyword.keyword == mock_keyword_data["keyword"]


def test_get_keyword(test_db_session: Session):
    """Test retrieving a keyword by ID."""
    keyword_in = KeywordCreate(**mock_keyword_data)
    created_keyword = create_keyword(test_db_session, keyword_in)

    fetched_keyword = get_keyword(test_db_session, created_keyword.keyword_id)
    assert fetched_keyword.keyword_id == created_keyword.keyword_id
    assert fetched_keyword.keyword == created_keyword.keyword


def test_get_keywords(test_db_session: Session):
    """Test retrieving a list of keywords with pagination."""
    keyword_data_list = [
        KeywordCreate(keyword="keyword1"),
        KeywordCreate(keyword="keyword2"),
        KeywordCreate(keyword="keyword3")
    ]

    for keyword_data in keyword_data_list:
        create_keyword(test_db_session, keyword_data)

    keywords = get_keywords(test_db_session, skip=0, limit=2)
    assert len(keywords) == 2  # Limit set to 2


def test_update_keyword(test_db_session: Session):
    """Test updating a keyword."""
    keyword_in = KeywordCreate(**mock_keyword_data)
    created_keyword = create_keyword(test_db_session, keyword_in)

    update_data = KeywordUpdate(keyword="updated_keyword")
    updated_keyword = update_keyword(test_db_session, created_keyword.keyword_id, update_data)

    assert updated_keyword.keyword == "updated_keyword"


def test_delete_keyword(test_db_session: Session):
    """Test deleting a keyword."""
    keyword_in = KeywordCreate(**mock_keyword_data)
    created_keyword = create_keyword(test_db_session, keyword_in)

    deleted_keyword = delete_keyword(test_db_session, created_keyword.keyword_id)
    assert deleted_keyword.keyword_id == created_keyword.keyword_id

    with pytest.raises(HTTPException) as exc_info:
        get_keyword(test_db_session, created_keyword.keyword_id)
    assert exc_info.value.status_code == 404


def test_get_keyword_not_found(test_db_session: Session):
    """Test error handling when a keyword is not found."""
    with pytest.raises(HTTPException) as exc_info:
        get_keyword(test_db_session, keyword_id=9999)  # Non-existent keyword ID
    assert exc_info.value.status_code == 404


def test_delete_keyword_not_found(test_db_session: Session):
    """Test error handling when trying to delete a non-existent keyword."""
    with pytest.raises(HTTPException) as exc_info:
        delete_keyword(test_db_session, keyword_id=9999)
    assert exc_info.value.status_code == 404
