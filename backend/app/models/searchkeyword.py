# app/models/searchkeyword.py
from sqlalchemy import Column, Integer, ForeignKey
from app.db.session import Base

class SearchKeyword(Base):
    __tablename__ = "SearchKeyword"

    search_keyword_id = Column(Integer, primary_key=True, index=True)
    search_id = Column(Integer, ForeignKey("Search.search_id"))
    keyword_id = Column(Integer, ForeignKey("Keyword.keyword_id"))