# backend/tests/test_db.py
import pytest
from sqlalchemy.exc import IntegrityError
from app.db.session import SessionLocal
from app.models import User, Role, Article, Search
from app.crud.user import create_user
from app.schemas.user import UserCreate

@pytest.fixture(scope="module")
def db():
    """Set up the database connection for testing."""
    db = SessionLocal()
    yield db
    db.close()

def test_role_table_exists(db):
    """Test if the Role table is created and accessible."""
    roles = db.query(Role).all()
    assert isinstance(roles, list)  # Expecting an empty or populated list
    assert len(roles) >= 0  # No error, table should exist

def test_user_creation(db):
    """Test if a user can be created and retrieved successfully."""
    user_data = UserCreate(username="testuser", password="testpass", email="test@example.com")
    user = create_user(db=db, user=user_data)
    
    # Fetch the user again to check
    fetched_user = db.query(User).filter(User.username == "testuser").first()
    assert fetched_user is not None
    assert fetched_user.username == "testuser"
    assert fetched_user.email == "test@example.com"

def test_article_creation_with_user(db):
    """Test article creation with valid user association."""
    # Create a new user first
    user_data = UserCreate(username="articleuser", password="password123", email="articleuser@example.com")
    user = create_user(db=db, user=user_data)
    
    # Create an article associated with the user
    article = Article(user_id=user.user_id, title="Test Article", source_id=1, search_id=1)
    db.add(article)
    db.commit()

    # Check that article is linked with the user
    fetched_article = db.query(Article).filter(Article.title == "Test Article").first()
    assert fetched_article is not None
    assert fetched_article.user_id == user.user_id
    assert fetched_article.title == "Test Article"

def test_foreign_key_constraint(db):
    """Test foreign key constraint by attempting to create an article with a non-existent source."""
    with pytest.raises(IntegrityError):
        article = Article(title="Test Article", source_id=9999, search_id=1)  # Invalid source_id
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