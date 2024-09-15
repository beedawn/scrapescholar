# app/models/__init__.py

from app.db.session import Base  # Import Base from session

# Import all models here so that Base has them before being used for creating tables
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