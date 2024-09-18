# app/crud/keyword.py
from sqlalchemy.orm import Session
from app.models.keyword import Keyword
from app.schemas.keyword import KeywordCreate, KeywordUpdate

def get_keyword(db: Session, keyword_id: int):
    return db.query(Keyword).filter(Keyword.keyword_id == keyword_id).first()

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
    if db_keyword:
        for key, value in keyword.dict(exclude_unset=True).items():
            setattr(db_keyword, key, value)
        db.commit()
        db.refresh(db_keyword)
    return db_keyword

def delete_keyword(db: Session, keyword_id: int):
    db_keyword = db.query(Keyword).filter(Keyword.keyword_id == keyword_id).first()
    if db_keyword:
        db.delete(db_keyword)
        db.commit()
    return db_keyword