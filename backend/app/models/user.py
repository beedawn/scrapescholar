# app/models/user.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("Role.role_id"))
    email = Column(String(100), unique=True)
    registration_date = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="users")
    articles = relationship("Article", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    article_scores = relationship("ArticleScore", foreign_keys="ArticleScore.user_id", back_populates="user")
    collaborations = relationship("Collaboration", back_populates="user")
    search_shares = relationship("SearchShare", foreign_keys="SearchShare.shared_with_user_id", back_populates="shared_with_user")
    search_shares_by = relationship("SearchShare", foreign_keys="SearchShare.shared_by_user_id", back_populates="shared_by_user")
    research_question_scores = relationship("ResearchQuestionScore", back_populates="last_updated_by")
    searches = relationship("Search", back_populates="user")