from sqlalchemy.orm import Session
from app.models.search import Search
from app.schemas.search import SearchCreate, SearchUpdate
from fastapi import HTTPException


def get_search(db: Session, search_id: int):
    search = db.query(Search).filter(Search.search_id == search_id).first()
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    return search


def get_search_by_title(db: Session, title: str):
    search = db.query(Search).filter(Search.title == title).first()
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    return search


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
    if not db_search:
        raise HTTPException(status_code=404, detail="Search not found")
    for key, value in search.dict(exclude_unset=True).items():
        setattr(db_search, key, value)
    db.commit()
    db.refresh(db_search)
    return db_search


def delete_search(db: Session, search_id: int):
    search = db.query(Search).filter(Search.search_id == search_id).first()
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    db.delete(search)
    db.commit()
    return search
