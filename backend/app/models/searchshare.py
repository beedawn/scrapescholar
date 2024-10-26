# app/models/searchshare.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class SearchShare(Base):
    __tablename__ = "SearchShare"

    share_id = Column(Integer, primary_key=True, index=True)
    search_id = Column(Integer, ForeignKey("Search.search_id"))
    shared_with_user_id = Column(Integer, ForeignKey("User.user_id"))
    shared_by_user_id = Column(Integer, ForeignKey("User.user_id"))
    share_date = Column(DateTime, default=datetime.utcnow)

    shared_with_user = relationship("User", foreign_keys=[shared_with_user_id], back_populates="search_shares")
    shared_by_user = relationship("User", foreign_keys=[shared_by_user_id], back_populates="search_shares_by")
