# app/crud/searchshare.py
from sqlalchemy.orm import Session
from app.models.searchshare import SearchShare
from app.schemas.searchshare import SearchShareCreate

def get_search_share(db: Session, share_id: int):
    return db.query(SearchShare).filter(SearchShare.share_id == share_id).first()

def get_search_shares(db: Session, skip: int = 0, limit: int = 10):
    return db.query(SearchShare).offset(skip).limit(limit).all()

def create_search_share(db: Session, search_share: SearchShareCreate):
    db_search_share = SearchShare(**search_share.dict())
    db.add(db_search_share)
    db.commit()
    db.refresh(db_search_share)
    return db_search_share

def delete_search_share(db: Session, share_id: int):
    db_search_share = db.query(SearchShare).filter(SearchShare.share_id == share_id).first()
    if db_search_share:
        db.delete(db_search_share)
        db.commit()
    return db_search_share