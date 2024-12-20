import pytest
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from app.crud.user_data import get_user_data, create_user_data, update_user_data, delete_user_data
from app.crud.article import create_article, delete_article
from app.crud.search import create_search, delete_search
from app.schemas.user_data import UserDataUpdate
from app.schemas.article import ArticleCreate
from app.schemas.search import SearchCreate
from app.db.session import SessionLocal
from app.crud.user import get_user_by_username
from tests.integration.tools.get_cookie import get_cookie

session = get_cookie()


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


def setup(test_db_session):
    test_user = get_user_by_username(test_db_session, "testuser")
    search = SearchCreate(user_id=test_user.user_id, search_keywords=None, Status=None, title="test search")
    created_search = create_search(test_db_session, search)
    mock_article_data.update({"search_id": created_search.search_id})
    article_in = ArticleCreate(**mock_article_data)
    created_article = create_article(test_db_session, article_in, user_id=test_user.user_id)

    created_user_data = create_user_data(
        test_db_session,
        user_id=test_user.user_id,
        article_id=created_article.article_id
    )
    return created_article, created_user_data, created_search


def teardown(test_db_session, created_article, created_user_data, created_search):
    delete_user_data(test_db_session, created_user_data.userdata_id)
    delete_article(test_db_session, created_article.article_id)
    delete_search(test_db_session, created_search.search_id)


def test_create_user_data(test_db_session: Session):
    """Test creating a new user data entry."""
    test_user = get_user_by_username(test_db_session, "testuser")
    created_article, created_user_data, created_search = setup(test_db_session)
    assert created_user_data.user_id == test_user.user_id
    assert created_user_data.article_id == created_article.article_id
    teardown(test_db_session, created_article, created_user_data, created_search)


def test_get_user_data(test_db_session: Session):
    """Test retrieving a user data entry by article_id."""

    created_article, created_user_data, created_search = setup(test_db_session)

    fetched_user_data = get_user_data(test_db_session, article_id=created_user_data.article_id)
    assert fetched_user_data.article_id == created_user_data.article_id
    teardown(test_db_session, created_article, created_user_data, created_search)


def test_get_user_data_not_found(test_db_session: Session):
    """Test error handling when a user data entry is not found by article_id."""
    with pytest.raises(HTTPException) as exc_info:
        get_user_data(test_db_session, article_id=9999)
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_update_user_data(test_db_session: Session):
    """Test updating an existing user data entry."""
    created_article, created_user_data, created_search = setup(test_db_session)

    user_role = "Professor"

    update_data = UserDataUpdate(
        article_id=created_user_data.article_id,
        relevancy_color="blue",
        methodology=4,
        clarity=5,
        transparency=4,
        completeness=5
    )
    access_token = session.cookies.get('access_token')

    updated_user_data = await update_user_data(test_db_session, update_data, user_role, access_token)

    assert updated_user_data.relevancy_color == "blue"
    assert updated_user_data.methodology == 4
    assert updated_user_data.clarity == 5
    assert updated_user_data.transparency == 4
    assert updated_user_data.completeness == 5

    teardown(test_db_session, created_article, created_user_data, created_search)


@pytest.mark.asyncio
async def test_update_user_data_not_found(test_db_session: Session):
    """Test updating a non-existent user data entry."""
    user_role = "Professor"

    update_data = UserDataUpdate(
        article_id=9999,  # Non-existent article_id
        relevancy_color="blue",
        methodology=4,
        clarity=5,
        transparency=4,
        completeness=5
    )
    access_token = session.cookies.get('access_token')

    with pytest.raises(HTTPException) as exc_info:
        await update_user_data(test_db_session, update_data, user_role, access_token)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Userdata not found in put, user not valid in db"
