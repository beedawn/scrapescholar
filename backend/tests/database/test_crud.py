# backend/tests/test_crud.py

import pytest
from app.crud.article import create_article, get_article, update_article, delete_article, get_articles
from app.models.user_data import UserData
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

# Test for deleting a non-existent article
def test_delete_article_not_found(test_db_session: Session):
    with pytest.raises(HTTPException) as exc_info:
        delete_article(test_db_session, article_id=9999)
    assert exc_info.value.status_code == 404

# Test for error handling in `get_article`
def test_get_article_not_found(test_db_session: Session):
    with pytest.raises(HTTPException) as exc_info:
        get_article(test_db_session, article_id=9999)  # Non-existent ID
    assert exc_info.value.status_code == 404

def test_get_articles_pagination(test_db_session: Session):
    """Test retrieving a paginated list of articles."""

    # Step 1: Clear existing UserData and Article entries in the database (if not using a rollback approach)
    test_db_session.query(UserData).delete()
    test_db_session.query(Article).delete()
    test_db_session.commit()

    # Step 2: Create a user and search entry for setting up foreign key references
    user_in = UserCreate(**mock_user_data)
    created_user = create_user(test_db_session, user_in)
    search_in = SearchCreate(user_id=created_user.user_id, **mock_search_data)
    created_search = create_search(test_db_session, search_in)

    # Step 3: Create multiple articles to test pagination
    article_data_list = [
        ArticleCreate(search_id=created_search.search_id, **{**mock_article_data, "title": "First Article"}),
        ArticleCreate(search_id=created_search.search_id, **{**mock_article_data, "title": "Second Article"}),
        ArticleCreate(search_id=created_search.search_id, **{**mock_article_data, "title": "Third Article"})
    ]
    for article_data in article_data_list:
        create_article(test_db_session, article_data, user_id=created_user.user_id)

    # Step 4: Retrieve a paginated list of articles
    skip = 0
    limit = 2
    articles = get_articles(test_db_session, skip=skip, limit=limit)

    # Step 5: Verify the number of articles returned matches the limit and order
    assert len(articles) == limit
    assert articles[0].title == "First Article"
    assert articles[1].title == "Second Article"

    # Step 6: Test the pagination by changing the `skip` parameter
    articles_with_skip = get_articles(test_db_session, skip=2, limit=limit)
    assert len(articles_with_skip) == 1
    assert articles_with_skip[0].title == "Third Article"