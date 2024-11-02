# backend/tests/database/test_crud_user_data.py

import pytest
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from app.crud.user_data import get_user_data, create_user_data, update_user_data
from app.crud.article import create_article
from app.schemas.user_data import UserDataUpdate
from app.schemas.article import ArticleCreate
from app.db.session import SessionLocal

@pytest.fixture
def test_db_session():
    """Fixture to provide a database session with rollback for testing."""
    db = SessionLocal()
    db.begin_nested()
    yield db
    db.rollback()
    db.close()

mock_article_data = {
    "source_id": 1,
    "search_id": 1,
    "title": "Test Article",
    "date": "2024-12-31",
    "link": "http://example.com/test_article",
    "relevance_score": 95.0,
    "abstract": "This is a test article.",
    "citedby": 100,
    "document_type": "Journal",
    "doi": "10.1000/testdoi"
}

def test_create_user_data(test_db_session: Session):
    """Test creating a new user data entry."""

    # Step 1: Create an Article entry for the foreign key reference
    article_in = ArticleCreate(**mock_article_data)
    created_article = create_article(test_db_session, article_in, user_id=1)

    # Step 2: Create a UserData entry using the article_id
    created_user_data = create_user_data(
        test_db_session,
        user_id=1,
        article_id=created_article.article_id
    )
    assert created_user_data.user_id == 1
    assert created_user_data.article_id == created_article.article_id

def test_get_user_data(test_db_session: Session):
    """Test retrieving a user data entry by article_id."""

    # Step 1: Create an Article entry for the foreign key reference
    article_in = ArticleCreate(**mock_article_data)
    created_article = create_article(test_db_session, article_in, user_id=1)

    # Step 2: Create a UserData entry using the article_id
    created_user_data = create_user_data(
        test_db_session,
        user_id=1,
        article_id=created_article.article_id
    )

    # Retrieve the UserData entry
    fetched_user_data = get_user_data(test_db_session, article_id=created_user_data.article_id)
    assert fetched_user_data.article_id == created_user_data.article_id

def test_get_user_data_not_found(test_db_session: Session):
    """Test error handling when a user data entry is not found by article_id."""
    with pytest.raises(HTTPException) as exc_info:
        get_user_data(test_db_session, article_id=9999)
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_update_user_data(test_db_session: Session):
    """Test updating an existing user data entry."""
    article_in = ArticleCreate(**mock_article_data)
    created_article = create_article(test_db_session, article_in, user_id=1)

    created_user_data = create_user_data(
        test_db_session,
        user_id=1,
        article_id=created_article.article_id
    )

    # Update the user data entry with integer values
    update_data = UserDataUpdate(
        article_id=created_user_data.article_id,
        relevancy_color="blue",
        methodology=4,
        clarity=5,
        transparency=4,
        completeness=5
    )
    updated_user_data = await update_user_data(test_db_session, update_data)

    # Verify the updated fields
    assert updated_user_data.relevancy_color == "blue"
    assert updated_user_data.methodology == 4
    assert updated_user_data.clarity == 5
    assert updated_user_data.transparency == 4
    assert updated_user_data.completeness == 5


@pytest.mark.asyncio
async def test_update_user_data_not_found(test_db_session: Session):
    """Test updating a non-existent user data entry."""
    update_data = UserDataUpdate(
        article_id=9999,  # Non-existent article_id
        relevancy_color="blue",
        methodology="4",
        clarity="5",
        transparency="4",
        completeness="5"
    )
    with pytest.raises(HTTPException) as exc_info:
        await update_user_data(test_db_session, update_data)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Userdata not found in put, user not valid in db"