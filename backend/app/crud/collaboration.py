# app/crud/collaboration.py
from sqlalchemy.orm import Session
from app.models.collaboration import Collaboration
from app.schemas.collaboration import CollaborationCreate
from fastapi import HTTPException

def get_collaboration(db: Session, collaboration_id: int):
    collaboration = db.query(Collaboration).filter(Collaboration.collaboration_id == collaboration_id).first()
    if not collaboration:
        raise HTTPException(status_code=404, detail="Collaboration not found")
    return collaboration

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
    if not db_collaboration:
        raise HTTPException(status_code=404, detail="Collaboration not found")
    db.delete(db_collaboration)
    db.commit()
    return db_collaboration