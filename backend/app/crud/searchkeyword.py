# app/crud/searchkeyword.py
from sqlalchemy.orm import Session
from app.models.searchkeyword import SearchKeyword
from app.schemas.searchkeyword import SearchKeywordCreate

def get_search_keyword(db: Session, search_keyword_id: int):
    return db.query(SearchKeyword).filter(SearchKeyword.search_keyword_id == search_keyword_id).first()

def get_search_keywords(db: Session, skip: int = 0, limit: int = 10):
    return db.query(SearchKeyword).offset(skip).limit(limit).all()

def create_search_keyword(db: Session, search_keyword: SearchKeywordCreate):
    db_search_keyword = SearchKeyword(**search_keyword.dict())
    db.add(db_search_keyword)
    db.commit()
    db.refresh(db_search_keyword)
    return db_search_keyword

def delete_search_keyword(db: Session, search_keyword_id: int):
    db_search_keyword = db.query(SearchKeyword).filter(SearchKeyword.search_keyword_id == search_keyword_id).first()
    if db_search_keyword:
        db.delete(db_search_keyword)
        db.commit()
    return db_search_keyword