import pytest
from sqlalchemy.orm import Session
from app.crud.comment import (
    get_comment,
    get_comments,

    create_comment,
    update_comment,
    delete_comment,
)

from app.crud.article import create_article, delete_article
from app.crud.user import get_user_by_username
from app.schemas.article import ArticleCreate
from app.schemas.comment import CommentCreate, CommentUpdate
from datetime import date
from app.schemas.search import SearchCreate
from app.crud.search import create_search, delete_search
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


mock_comment_data = {
    "comment_text": "test comment"
}

mock_article_data = {
    "source_id": 1,
    "title": "test",
    "date": date.today()
}


def cleanup(test_db_session, created_comment, article, search):
    delete_comment(test_db_session, created_comment["comment_id"])
    delete_article(test_db_session, article.article_id)
    delete_search(test_db_session, search.search_id)


def setup(test_db_session):
    user = get_user_by_username(test_db_session, "testuser")
    search = SearchCreate(user_id=user.user_id, title="test")
    created_search = create_search(test_db_session, search)
    new_article = ArticleCreate(**mock_article_data, search_id=created_search.search_id)
    article = create_article(test_db_session, new_article, user.user_id)
    return article, user, created_search


def test_create_comment(test_db_session: Session):
    article, user, search = setup(test_db_session)
    comment_in = CommentCreate(**mock_comment_data)
    created_comment = create_comment(test_db_session, article.article_id, comment_in, user.user_id)
    assert created_comment["comment_text"] == mock_comment_data["comment_text"]
    cleanup(test_db_session, created_comment, article,search)


def test_get_comment(test_db_session: Session):
    article, user, search = setup(test_db_session)
    comment_in = CommentCreate(**mock_comment_data)
    created_comment = create_comment(test_db_session, article.article_id, comment_in, user.user_id)

    fetched_comment = get_comment(test_db_session, created_comment["comment_id"])

    assert fetched_comment.comment_id == created_comment["comment_id"]
    assert fetched_comment.comment_text == created_comment["comment_text"]
    cleanup(test_db_session, created_comment, article, search)

def test_get_comments(test_db_session: Session):
    article, user, search = setup(test_db_session)
    comment_data_list = [
        CommentCreate(**mock_comment_data),
        CommentCreate(**mock_comment_data),
        CommentCreate(**mock_comment_data)
    ]
    comment_list = []
    for comment_data in comment_data_list:
        created_comment=create_comment(test_db_session, article.article_id, comment_data, user.user_id)
        comment_list.append(created_comment)
    comments = get_comments(test_db_session, skip=0, limit=2)
    assert len(comments) == 2  # Limit set to 2
    for comment_data in comment_list:
        delete_comment(test_db_session, comment_data["comment_id"])
    delete_article(test_db_session, article.article_id)
    delete_search(test_db_session, search.search_id)


def test_update_comment(test_db_session: Session):
    article, user, search = setup(test_db_session)
    comment_in = CommentCreate(**mock_comment_data)
    created_comment = create_comment(test_db_session, article.article_id, comment_in, user.user_id)

    update_data = CommentUpdate(comment_text="updated_comment")
    updated_comment = update_comment(test_db_session, created_comment["comment_id"], update_data)

    assert updated_comment["comment_text"] == "updated_comment"
    cleanup(test_db_session, created_comment, article, search)


def test_delete_comment(test_db_session: Session):
    article, user, search = setup(test_db_session)
    comment_in = CommentCreate(**mock_comment_data)
    created_comment = create_comment(test_db_session, article.article_id, comment_in, user.user_id)

    deleted_comment = delete_comment(test_db_session, created_comment["comment_id"])
    assert deleted_comment.comment_id == created_comment["comment_id"]

    with pytest.raises(HTTPException) as exc_info:
        get_comment(test_db_session, created_comment["comment_id"])
    assert exc_info.value.status_code == 404
    delete_article(test_db_session, article.article_id)
    delete_search(test_db_session, search.search_id)

