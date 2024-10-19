# app/models/user_data.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class UserData(Base):
    __tablename__ = "UserData"

    userdata_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.user_id"))
    article_id = Column(Integer, ForeignKey("Article.article_id"))
    relevancy_color = Column(String(20), default="")
    methodology = Column(Integer, default=0)
    clarity = Column(Integer, default=0)
    transparency = Column(Integer, default=0)
    completeness = Column(Integer, default=0)
    evaluation_criteria = Column(String, nullable=True)
