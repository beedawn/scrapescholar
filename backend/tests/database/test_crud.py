# backend/tests/test_crud.py
import pytest
from app.crud.article import create_article, get_article, update_article, delete_article
from app.crud.search import create_search
from app.crud.user import create_user
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.schemas.search import SearchCreate
from app.schemas.user import UserCreate
from app.models.article import Article
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from fastapi.exceptions import HTTPException

# Mock data for user
mock_user_data = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testpassword"
}

# Mock data for search (required for foreign key reference)
mock_search_data = {
    "search_keywords": ["Test", "Article"],
    "title": "Test Search"
}

# Mock data for article
mock_article_data = {
    "title": "Test Article",
    "date": "2024-12-31",
    "link": "http://example.com/test_article",
    "relevance_score": 95,
    "evaluation_criteria": "High",
    "abstract": "This is a test article.",
    "citedby": 100,
    "document_type": "Journal",
    "source_id": 1
}

@pytest.fixture
def test_db_session():
    """Fixture to provide a database session for testing"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_article(test_db_session: Session):
    # Step 1: Create a user entry (required for user_id foreign key)
    user_in = UserCreate(**mock_user_data)
    created_user = create_user(test_db_session, user_in)

    # Step 2: Create a search entry (required for search_id foreign key)
    search_in = SearchCreate(user_id=created_user.user_id, **mock_search_data)
    created_search = create_search(test_db_session, search_in)

    # Step 3: Insert the article with the newly created search_id and user_id
    article_in = ArticleCreate(search_id=created_search.search_id, **mock_article_data)
    created_article = create_article(test_db_session, article_in, user_id=created_user.user_id)

    # Step 4: Validate the article creation
    assert created_article.title == mock_article_data["title"]
    assert created_article.relevance_score == mock_article_data["relevance_score"]

def test_get_article_by_id(test_db_session: Session):
    """Test retrieving an article by ID"""

    # Step 1: Create a user entry (required for user_id foreign key)
    user_in = UserCreate(**mock_user_data)
    created_user = create_user(test_db_session, user_in)

    # Step 2: Create a search entry (required for search_id foreign key)
    search_in = SearchCreate(user_id=created_user.user_id, **mock_search_data)
    created_search = create_search(test_db_session, search_in)

    # Step 3: Create an article for retrieval
    article_in = ArticleCreate(search_id=created_search.search_id, **mock_article_data)
    created_article = create_article(test_db_session, article_in, user_id=created_user.user_id)  # Pass user_id

    # Step 4: Retrieve the article by its ID
    article = get_article(test_db_session, created_article.article_id)
    
    # Step 5: Validate the retrieved article
    assert article is not None
    assert article.title == mock_article_data["title"]

def test_update_article(test_db_session: Session):
    """Test updating an article"""

    # Step 1: Create a user entry (required for user_id foreign key)
    user_in = UserCreate(**mock_user_data)
    created_user = create_user(test_db_session, user_in)

    # Step 2: Create a search entry (required for search_id foreign key)
    search_in = SearchCreate(user_id=created_user.user_id, **mock_search_data)
    created_search = create_search(test_db_session, search_in)

    # Step 3: Create an article
    article_in = ArticleCreate(search_id=created_search.search_id, **mock_article_data)
    created_article = create_article(test_db_session, article_in, user_id=created_user.user_id)  # Pass user_id

    # Step 4: Update the article with new data
    update_data = ArticleUpdate(title="Updated Title", relevance_score=99)
    updated_article = update_article(test_db_session, article_id=created_article.article_id, article=update_data)

    # Step 5: Validate the updated article
    assert updated_article.title == "Updated Title"
    assert updated_article.relevance_score == 99


def test_delete_article(test_db_session: Session):
    """Test deleting an article"""

    # Step 1: Create a user entry (required for user_id foreign key)
    user_in = UserCreate(**mock_user_data)
    created_user = create_user(test_db_session, user_in)

    # Step 2: Create a search entry (required for search_id foreign key)
    search_in = SearchCreate(user_id=created_user.user_id, **mock_search_data)
    created_search = create_search(test_db_session, search_in)

    # Step 3: Create an article
    article_in = ArticleCreate(search_id=created_search.search_id, **mock_article_data)
    created_article = create_article(test_db_session, article_in, user_id=created_user.user_id)  # Pass user_id

    # Step 4: Delete the article by ID
    deleted_article = delete_article(test_db_session, article_id=created_article.article_id)

    # Step 5: Validate the deletion (usually returns None or the deleted entity)
    assert deleted_article is None or deleted_article.article_id == created_article.article_id

    # Step 6: Ensure that the article is no longer in the database
    try:
        fetched_article = get_article(test_db_session, created_article.article_id)
    except HTTPException as e:
        assert e.status_code == 404