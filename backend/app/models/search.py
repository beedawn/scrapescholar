# app/models/search.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Search(Base):
    __tablename__ = "Search"

    search_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.user_id"))
    search_date = Column(TIMESTAMP)
    search_keywords = Column(ARRAY(String))
    status = Column(String(20), default='active')

    user = relationship("User", back_populates="searches")
    articles = relationship("Article", back_populates="search")    