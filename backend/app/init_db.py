# backend/app/init_db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.models import User, Article, Source, Role, Search
from app.dependencies import get_db_uri
from app.schemas.user import UserCreate
from app.schemas.source import SourceCreate
from app.schemas.search import SearchCreate
from app.crud.user import create_user
from app.crud.source import create_source
from app.crud.search import create_search
from dotenv import load_dotenv

load_dotenv()
test_user=os.getenv("TEST_USER")
test_password = os.getenv("TEST_PASSWORD")

# Retrieve the database URI
SQLALCHEMY_DATABASE_URL = get_db_uri()

# Create a new SQLAlchemy engine instance
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize the database and insert test data if the environment is set for testing.
    """
    # Import all the models to register them on the metadata
    from app.models.user import User
    from app.models.role import Role
    from app.models.keyword import Keyword
    from app.models.source import Source
    from app.models.search import Search
    from app.models.article import Article
    from app.models.comment import Comment
    from app.models.collaboration import Collaboration
    from app.models.articlescore import ArticleScore
    from app.models.searchshare import SearchShare
    from app.models.searchkeyword import SearchKeyword
    from app.models.researchquestion import ResearchQuestion
    from app.models.researchquestionmapping import ResearchQuestionMapping
    from app.models.researchquestionscore import ResearchQuestionScore

    # Create the database tables
    Base.metadata.create_all(bind=engine)

    # Check if we are in the test environment
    db: SessionLocal = SessionLocal()
    try:
        db_name = os.getenv("POSTGRES_DB")
        if "scrapescholartestdb" in db_name:
            print("Test environment detected, inserting test data...")
            insert_test_data(db)
        else:
            print("Not in a test environment, skipping test data insertion.")
    except Exception as e:
        print(f"Error initializing test data: {e}")
    finally:
        db.close()

def insert_test_data(db):
    """
    Insert test data into the database for testing purposes.
    """
    # Insert Roles (if needed)
    admin_role = Role(role_name="admin")
    user_role = Role(role_name="user")
    db.add_all([admin_role, user_role])
    db.commit()

    # Insert a test User
    user_data = UserCreate(
        username=test_user,
        password=test_password,
        email="testuser@example.com"
    )
    user = create_user(db=db, user=user_data)

    # Insert a test Source
    source_data = SourceCreate(
        name="Sample Source",
        api_endpoint="http://api.example.com",
        scrape_source_url="http://scrape.example.com"
    )
    source = create_source(db=db, source=source_data)

    # Insert a test Search associated with the User
    search_data = SearchCreate(
        user_id=user.user_id,
        search_keywords=["test", "example"]
    )
    create_search(db=db, search=search_data)

    db.commit()
    print("Test data inserted successfully.")

if __name__ == "__main__":
    init_db()
    print("Database initialized and tables created.")