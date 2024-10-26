# app/models/articlescore.py

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class ArticleScore(Base):
    __tablename__ = "ArticleScore"

    article_score_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    article_id = Column(Integer, ForeignKey("Article.article_id"), nullable=False)
    score = Column(Float, nullable=False)
    last_updated_by_user_id = Column(Integer, ForeignKey("User.user_id"))
    evaluation_date = Column(DateTime, default=datetime.utcnow)
    last_updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id], back_populates="article_scores")
    article = relationship("Article", back_populates="article_scores")
    last_updated_by = relationship("User", foreign_keys=[last_updated_by_user_id])
