# app/crud/keyword.py
from sqlalchemy.orm import Session
from app.models.keyword import Keyword
from app.schemas.keyword import KeywordCreate, KeywordUpdate
from fastapi import HTTPException

def get_keyword(db: Session, keyword_id: int):
    keyword = db.query(Keyword).filter(Keyword.keyword_id == keyword_id).first()
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return keyword

def get_keywords(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Keyword).offset(skip).limit(limit).all()

def create_keyword(db: Session, keyword: KeywordCreate):
    db_keyword = Keyword(**keyword.dict())
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword

def update_keyword(db: Session, keyword_id: int, keyword: KeywordUpdate):
    db_keyword = db.query(Keyword).filter(Keyword.keyword_id == keyword_id).first()
    if not db_keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    for key, value in keyword.dict(exclude_unset=True).items():
        setattr(db_keyword, key, value)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword

def delete_keyword(db: Session, keyword_id: int):
    db_keyword = db.query(Keyword).filter(Keyword.keyword_id == keyword_id).first()
    if not db_keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    db.delete(db_keyword)
    db.commit()
    return db_keyword