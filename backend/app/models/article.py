from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Article(Base):
    __tablename__ = "Article"

    article_id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("Source.source_id"))
    search_id = Column(Integer, ForeignKey("Search.search_id"))
    user_id = Column(Integer, ForeignKey("User.user_id"))   
    title = Column(String, nullable=False)
    author = Column(String, nullable=True)
    publication_date = Column(Date, nullable=True)
    journal = Column(String, nullable=True)
    url = Column(String, nullable=True)
    relevance_score = Column(Float, nullable=True)
    review_status = Column(String, nullable=True)
    abstract = Column(String, nullable=True)
    doi = Column(String, nullable=True)

    # Relationships
    source = relationship("Source", back_populates="articles")
    search = relationship("Search", back_populates="articles")
    comments = relationship("Comment", back_populates="article")
    article_scores = relationship("ArticleScore", back_populates="article")
    research_question_mappings = relationship("ResearchQuestionMapping", back_populates="article")
    user = relationship("User", back_populates="articles")