# app/crud/source.py
from sqlalchemy.orm import Session
from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate

def get_source(db: Session, source_id: int):
    return db.query(Source).filter(Source.source_id == source_id).first()

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
    if db_source:
        for key, value in source.dict(exclude_unset=True).items():
            setattr(db_source, key, value)
        db.commit()
        db.refresh(db_source)
    return db_source

def delete_source(db: Session, source_id: int):
    db_source = db.query(Source).filter(Source.source_id == source_id).first()
    if db_source:
        db.delete(db_source)
        db.commit()
    return db_source