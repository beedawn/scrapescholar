# app/crud/collaboration.py
from sqlalchemy.orm import Session
from app.models.collaboration import Collaboration
from app.schemas.collaboration import CollaborationCreate

def get_collaboration(db: Session, collaboration_id: int):
    return db.query(Collaboration).filter(Collaboration.collaboration_id == collaboration_id).first()

def get_collaborations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Collaboration).offset(skip).limit(limit).all()

def create_collaboration(db: Session, collaboration: CollaborationCreate):
    db_collaboration = Collaboration(**collaboration.dict())
    db.add(db_collaboration)
    db.commit()
    db.refresh(db_collaboration)
    return db_collaboration

def delete_collaboration(db: Session, collaboration_id: int):
    db_collaboration = db.query(Collaboration).filter(Collaboration.collaboration_id == collaboration_id).first()
    if db_collaboration:
        db.delete(db_collaboration)
        db.commit()
    return db_collaboration