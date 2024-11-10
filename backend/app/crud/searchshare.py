# app/crud/searchshare.py
from sqlalchemy.orm import Session
from app.models.searchshare import SearchShare
from app.schemas.searchshare import SearchShareCreate
from fastapi import HTTPException


def get_search_share(db: Session, share_id: int):
    share = db.query(SearchShare).filter(SearchShare.share_id == share_id).first()
    if not share:
        raise HTTPException(status_code=404, detail="Search share not found")
    return share

def get_search_share_by_search(db: Session, search_id: int):
    share = db.query(SearchShare).filter(SearchShare.search_id == search_id).all()
    if not share:
        share = None
    return share

def get_search_shares(db: Session, skip: int = 0, limit: int = 10):
    return db.query(SearchShare).offset(skip).limit(limit).all()


def create_search_share(db: Session, search_share: SearchShareCreate):
    db_search_share = SearchShare(**search_share.dict())
    db.add(db_search_share)
    db.commit()
    db.refresh(db_search_share)
    return db_search_share


def delete_search_share(db: Session, share_id: int):
    share = db.query(SearchShare).filter(SearchShare.share_id == share_id).first()
    if not share:
        raise HTTPException(status_code=404, detail="Search share not found")
    db.delete(share)
    db.commit()
    return share
