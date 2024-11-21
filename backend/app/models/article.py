# app/models/article.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class Article(Base):
    __tablename__ = "Article"

    article_id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("Source.source_id", ondelete="CASCADE"), nullable=False)
    search_id = Column(Integer, ForeignKey("Search.search_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("User.user_id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String, nullable=False) 
    citedby = Column(Integer, nullable=True)
    date = Column(Date, nullable=True)
    abstract = Column(String, nullable=True)
    link = Column(String, nullable=True)
    relevance_score = Column(Float, nullable=True)
    document_type= Column(String, nullable=True)
    doi = Column(String, nullable=True)

    source = relationship("Source", back_populates="articles")
    search = relationship("Search", back_populates="articles")
    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")
    article_scores = relationship("ArticleScore", back_populates="article", cascade="all, delete-orphan")
    research_question_mappings = relationship("ResearchQuestionMapping", back_populates="article", cascade="all, delete-orphan")
    collaborations = relationship("Collaboration", back_populates="article", cascade="all, delete-orphan")
    user = relationship("User", back_populates="articles")
