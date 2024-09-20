# app/init_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.dependencies import get_db_uri

# Retrieve the database URI
SQLALCHEMY_DATABASE_URL = get_db_uri()

# Create a new SQLAlchemy engine instance
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
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

if __name__ == "__main__":
    init_db()
    print("Database initialized and tables created.")