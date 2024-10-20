# app/models/keyword.py
from sqlalchemy import Column, Integer, String
from app.db.session import Base


class Keyword(Base):
    __tablename__ = "Keyword"

    keyword_id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(255), nullable=False)
