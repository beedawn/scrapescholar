# backend/tests/test_db.py
import pytest
from sqlalchemy.exc import IntegrityError
from app.db.session import SessionLocal
from app.models import User, Role, Article, Search
from app.crud.user import create_user
from app.schemas.user import UserCreate

@pytest.fixture(scope="module")
def db():
    # Set up the database connection
    db = SessionLocal()
    yield db
    db.close()

def test_role_table_exists(db):
    """Test if the Role table is created and accessible."""
    roles = db.query(Role).all()
    assert isinstance(roles, list)  # Expecting an empty or populated list

def test_user_creation(db):
    """Test if a user can be created and retrieved successfully."""
    user_data = UserCreate(username="testuser", password="testpass", email="test@example.com", role_id=1)
    user = create_user(db=db, user=user_data)
    assert user.username == "testuser"
    assert user.email == "test@example.com"

def test_foreign_key_constraint(db):
    """Test foreign key constraint by attempting to create an article with a non-existent source."""
    with pytest.raises(IntegrityError):
        article = Article(title="Test Article", source_id=9999)  # Invalid source_id
        db.add(article)
        db.commit()

def test_article_table_insert(db):
    """Test insertion into the Article table."""
    article = Article(title="Sample Article", source_id=1, search_id=1)
    db.add(article)
    db.commit()
    assert article.article_id is not None

def test_search_table_exists(db):
    """Test if the Search table is created and accessible."""
    searches = db.query(Search).all()
    assert isinstance(searches, list)  # Expecting an empty or populated list