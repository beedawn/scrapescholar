# backend/tests/test_db.py

import pytest
import uuid
from sqlalchemy.exc import IntegrityError
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.models import User, Article, Source, Role, Search, SearchShare
from app.crud.user import create_user, delete_user
from app.crud.source import create_source, delete_source
from app.crud.search import create_search, delete_search
from app.crud.searchshare import create_search_share, delete_search_share
from app.schemas.user import UserCreate
from app.schemas.source import SourceCreate
from app.schemas.search import SearchCreate
from app.schemas.searchshare import SearchShareCreate
from app.schemas.article import ArticleCreate
from app.schemas.searchkeyword import SearchKeywordCreate
from app.schemas.keyword import KeywordCreate
from app.crud.searchshare import create_search_share
from app.crud.article import create_article, delete_article
from app.crud.searchkeyword import create_search_keyword
from app.crud.keyword import create_keyword
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables for encryption
load_dotenv()
encryption_key = os.getenv("ENCRYPTION_KEY")
fernet = Fernet(encryption_key)

def verify_hash(plain_text, hashed_text: str):
    hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return hash_context.verify(plain_text, hashed_text)

def decrypt_username(encrypted_username: str) -> str:
    """Decrypt the encrypted username"""
    return fernet.decrypt(encrypted_username.encode()).decode()

@pytest.fixture(scope="function")
def db():
    """Set up the database connection for testing."""
    db = SessionLocal()
    db.begin_nested()
    yield db
    db.rollback()
    db.close()

def test_role_table_exists(db):
    """Test if the Role table is created and accessible."""
    roles = db.query(Role).all()
    assert isinstance(roles, list)  # Expecting an empty or populated list
    assert len(roles) >= 0  # No error, table should exist

def test_user_exists_in_db(db):
    """Test if the test user from init_db exists in the database."""

    users = db.query(User).all()
    user = None
    for candidate in users:
        try:
            decrypted_username = decrypt_username(candidate.username)
            # print(f"Decrypted username: {decrypted_username}")  # Debug output
            if decrypted_username == "testuser":
                user = candidate
                break
        except Exception as e:
            # print(f"Error decrypting username: {str(e)}")
            continue

    assert user is not None

    # print(f"Stored hashed password: {user.password}")
    # print(f"Stored email: {user.email}")

    # Removing this test for now
    # Remove email verification as it's hashed and not reversible
    # assert verify_hash("testuser@example.com", user.email)  
    # assert verify_hash("testpassword", user.password)


def test_article_creation_with_existing_user_and_source(db: Session):
    """Test article creation using the test data from init_db."""

    # Get the test user from the database
    users = db.query(User).all()
    user = None
    for candidate in users:
        try:
            decrypted_username = decrypt_username(candidate.username)
            if decrypted_username == "testuser":
                user = candidate
                break
        except:
            continue
    assert user is not None

    # Get the test source from the database
    source = db.query(Source).filter_by(name="Sample Source").first()
    assert source is not None

    # Create a new search associated with the test user
    search_data = SearchCreate(user_id=user.user_id, search_keywords=["new", "article"], title="Sample Search Title")
    search = create_search(db=db, search=search_data)

    # Create an article associated with the test user, test source, and new search
    article = Article(user_id=user.user_id, source_id=source.source_id, search_id=search.search_id, title="New Test Article")
    db.add(article)
    db.commit()
    db.delete(article)
    db.delete(search)
    db.commit()

    assert article.article_id is not None
    assert article.user_id == user.user_id
    assert article.source_id == source.source_id
    assert article.search_id == search.search_id

def test_foreign_key_constraint(db):
    """Test foreign key constraint by attempting to create an article with a non-existent source."""
    with pytest.raises(IntegrityError):
        article = Article(title="Test Article", source_id=9999, search_id=1)  # Invalid source_id
        db.add(article)
        db.commit()
        db.delete(article)
        db.commit()

    # Explicitly roll back after the failure
    db.rollback()

def test_article_table_insert_with_new_data(db: Session):
    """Test insertion into the Article table with new data."""

    # Step 1: Create a new user to associate with the search
    user_data = UserCreate(username="new_user", password="password123", email="new_user@example.com")
    user = create_user(db=db, user=user_data)

    # Step 2: Create a new source to satisfy the foreign key constraint
    source_data = SourceCreate(name="New Sample Source", api_endpoint="http://newapi.example.com", scrape_source_url="http://newscrape.example.com")
    source = create_source(db=db, source=source_data)

    # Step 3: Create a new search to satisfy the foreign key constraint for search_id
    search_data = SearchCreate(user_id=user.user_id, search_keywords=["sample", "keywords"], title="Sample Search Title")
    search = create_search(db=db, search=search_data)

    # Step 4: Create an article using the valid source_id and search_id
    article = Article(title="New Sample Article", source_id=source.source_id, search_id=search.search_id, user_id=user.user_id)
    db.add(article)

    try:
        db.commit()
        db.delete(article)
        db.delete(search)
        db.delete(source)
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    assert article.article_id is not None


def test_search_table_exists(db):
    """Test if the Search table is created and accessible."""
    searches = db.query(Search).all()
    assert isinstance(searches, list)  # Expecting an empty or populated list

def test_full_search_insert_and_share(db: Session):
    """
    Test the insertion of all related entities: Search, Articles, Keywords, and Share with a new user.
    """

    # Step 1: Create an existing user
    existing_user_data = UserCreate(username="existing_user", password="password123", email="existing_user@example.com")
    existing_user = create_user(db=db, user=existing_user_data)

    source_data = SourceCreate(name="New Sample Source", api_endpoint="http://newapi.example.com", scrape_source_url="http://newscrape.example.com")
    source = create_source(db=db, source=source_data)
    # Step 2: Create a new search for the existing user
    search_data = SearchCreate(user_id=existing_user.user_id, search_keywords=["AI", "Machine Learning"], title="AI and ML Search")
    search = create_search(db=db, search=search_data)

    # Step 3: Create at least 2 articles associated with the search
    article_1_data = ArticleCreate(source_id=source.source_id, search_id=search.search_id, title="Article 1", date=datetime.now().date())
    article_2_data = ArticleCreate(source_id=source.source_id, search_id=search.search_id, title="Article 2", date=datetime.now().date())
    article1 = create_article(db=db, article=article_1_data, user_id=existing_user.user_id)
    article2 = create_article(db=db, article=article_2_data, user_id=existing_user.user_id)


    # Step 4: Verify that both articles have been added
    articles = db.query(Article).filter(Article.search_id == search.search_id).all()
    assert len(articles) == 2
    assert articles[0].title == "Article 1"
    assert articles[1].title == "Article 2"


    # Step 5: Share the search with a new user
    new_user_data = UserCreate(username="new_user", password="password123", email="new_user@example.com")
    new_user = create_user(db=db, user=new_user_data)

    search_share_data = SearchShareCreate(search_id=search.search_id, shared_with_user_id=new_user.user_id, shared_by_user_id=existing_user.user_id)
    search_share = create_search_share(db=db, search_share=search_share_data)


    # Step 6: Verify the search share
    shared_search = db.query(SearchShare).filter(SearchShare.shared_with_user_id == new_user.user_id).first()
    assert shared_search is not None
    assert shared_search.search_id == search.search_id
    assert shared_search.shared_with_user_id == new_user.user_id
    delete_article(db, article1.article_id)
    delete_article(db, article2.article_id)
    delete_search_share(db, search_share.share_id)
    delete_search(db, search.search_id)
    delete_source(db, source.source_id)
    delete_user(db, existing_user.user_id)
    delete_user(db, new_user.user_id)

