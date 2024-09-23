# app/models/comment.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Comment(Base):
    __tablename__ = "Comment"

    comment_id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("Article.article_id"))
    user_id = Column(Integer, ForeignKey("User.user_id"))
    comment_text = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    article = relationship("Article", back_populates="comments")
    user = relationship("User", back_populates="comments")