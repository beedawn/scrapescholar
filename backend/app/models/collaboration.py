from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class Collaboration(Base):
    __tablename__ = "Collaboration"

    collaboration_id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("Article.article_id"))
    user_id = Column(Integer, ForeignKey("User.user_id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    article = relationship("Article", back_populates="collaborations")
    user = relationship("User", back_populates="collaborations")
