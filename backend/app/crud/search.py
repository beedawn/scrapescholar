# app/crud/search.py
from sqlalchemy.orm import Session
from app.models.search import Search
from app.schemas.search import SearchCreate, SearchUpdate

def get_search(db: Session, search_id: int):
    return db.query(Search).filter(Search.search_id == search_id).first()

def get_searches(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Search).offset(skip).limit(limit).all()

def create_search(db: Session, search: SearchCreate):
    db_search = Search(**search.dict())
    db.add(db_search)
    db.commit()
    db.refresh(db_search)
    return db_search

def update_search(db: Session, search_id: int, search: SearchUpdate):
    db_search = db.query(Search).filter(Search.search_id == search_id).first()
    if db_search:
        for key, value in search.dict(exclude_unset=True).items():
            setattr(db_search, key, value)
        db.commit()
        db.refresh(db_search)
    return db_search

def delete_search(db: Session, search_id: int):
    db_search = db.query(Search).filter(Search.search_id == search_id).first()
    if db_search:
        db.delete(db_search)
        db.commit()
    return db_search