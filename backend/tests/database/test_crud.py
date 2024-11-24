import pytest
from app.crud.article import create_article, get_article, update_article, delete_article, get_articles
from app.models.user_data import UserData
from app.crud.search import create_search, delete_search
from app.crud.user import get_user_by_username
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.schemas.search import SearchCreate

from app.models.article import Article
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from fastapi.exceptions import HTTPException


mock_search_data = {
    "search_keywords": ["Test", "Article"],
    "title": "Test Search"
}


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


def setup(test_db_session):
    test_user = get_user_by_username(test_db_session, "testuser")
    search_in = SearchCreate(user_id=test_user.user_id, **mock_search_data)
    created_search = create_search(test_db_session, search_in)
    article_in = ArticleCreate(search_id=created_search.search_id, **mock_article_data)
    created_article = create_article(test_db_session, article_in, user_id=test_user.user_id)
    return created_search, created_article


def teardown(test_db_session, created_article, created_search):
    if created_article is not None:
        delete_article(test_db_session, created_article.article_id)
    delete_search(test_db_session, created_search.search_id)


def test_create_article(test_db_session: Session):
    created_search, created_article = setup(test_db_session)
    assert created_article.title == mock_article_data["title"]
    assert created_article.relevance_score == mock_article_data["relevance_score"]
    teardown(test_db_session, created_article, created_search)


def test_get_article_by_id(test_db_session: Session):
    """Test retrieving an article by ID"""

    created_search, created_article = setup(test_db_session)
    article = get_article(test_db_session, created_article.article_id)
    assert article is not None
    assert article.title == mock_article_data["title"]
    teardown(test_db_session, created_article, created_search)


def test_update_article(test_db_session: Session):
    """Test updating an article"""

    created_search, created_article = setup(test_db_session)
    update_data = ArticleUpdate(title="Updated Title", relevance_score=99)
    updated_article = update_article(test_db_session, article_id=created_article.article_id, article=update_data)
    assert updated_article.title == "Updated Title"
    assert updated_article.relevance_score == 99
    teardown(test_db_session, created_article, created_search)


def test_delete_article(test_db_session: Session):
    """Test deleting an article"""
    created_search, created_article = setup(test_db_session)
    deleted_article = delete_article(test_db_session, article_id=created_article.article_id)
    assert deleted_article is None or deleted_article.article_id == created_article.article_id

    try:
        get_article(test_db_session, created_article.article_id)
    except HTTPException as e:
        assert e.status_code == 404
    teardown(test_db_session, None, created_search)


def test_delete_article_not_found(test_db_session: Session):
    with pytest.raises(HTTPException) as exc_info:
        delete_article(test_db_session, article_id=9999)
    assert exc_info.value.status_code == 404


def test_get_article_not_found(test_db_session: Session):
    with pytest.raises(HTTPException) as exc_info:
        get_article(test_db_session, article_id=9999)  # Non-existent ID
    assert exc_info.value.status_code == 404


def test_get_articles_pagination(test_db_session: Session):
    """Test retrieving a paginated list of articles."""
    test_db_session.query(UserData).delete()
    test_db_session.query(Article).delete()
    test_db_session.commit()

    test_user = get_user_by_username(test_db_session, "testuser")
    created_search, created_article = setup(test_db_session)
    delete_article(test_db_session, article_id=created_article.article_id)

    article_data_list = [
        ArticleCreate(search_id=created_search.search_id, **{**mock_article_data, "title": "First Article"}),
        ArticleCreate(search_id=created_search.search_id, **{**mock_article_data, "title": "Second Article"}),
        ArticleCreate(search_id=created_search.search_id, **{**mock_article_data, "title": "Third Article"})
    ]
    article_list = []
    for article_data in article_data_list:
        created_article = create_article(test_db_session, article_data, user_id=test_user.user_id)
        article_list.append(created_article)

    skip = 0
    limit = 2
    articles = get_articles(test_db_session, skip=skip, limit=limit)

    assert len(articles) == limit
    assert articles[0].title == "First Article"
    assert articles[1].title == "Second Article"

    articles_with_skip = get_articles(test_db_session, skip=2, limit=limit)
    assert len(articles_with_skip) == 1
    assert articles_with_skip[0].title == "Third Article"

    for article in article_list:
        delete_article(test_db_session, article_id=article.article_id)
    teardown(test_db_session, None, created_search)
