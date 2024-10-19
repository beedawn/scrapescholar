# app/models/source.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base


class Source(Base):
    __tablename__ = "Source"

    source_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    api_endpoint = Column(String(255))
    scrape_source_url = Column(String(255))

    articles = relationship("Article", back_populates="source")
