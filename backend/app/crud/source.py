# app/crud/source.py
from sqlalchemy.orm import Session
from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate
from fastapi import HTTPException

def get_source(db: Session, source_id: int):
    source = db.query(Source).filter(Source.source_id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source

def get_sources(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Source).offset(skip).limit(limit).all()

def create_source(db: Session, source: SourceCreate):
    db_source = Source(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source

def update_source(db: Session, source_id: int, source: SourceUpdate):
    db_source = db.query(Source).filter(Source.source_id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")
    for key, value in source.dict(exclude_unset=True).items():
        setattr(db_source, key, value)
    db.commit()
    db.refresh(db_source)
    return db_source

def delete_source(db: Session, source_id: int):
    db_source = db.query(Source).filter(Source.source_id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")
    db.delete(db_source)
    db.commit()
    return db_source
