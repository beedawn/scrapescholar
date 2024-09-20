# app/crud/rsearchquestionmapping.py
from sqlalchemy.orm import Session
from app.models.researchquestionmapping import ResearchQuestionMapping
from app.schemas.researchquestionmapping import ResearchQuestionMappingCreate, ResearchQuestionMappingUpdate
from fastapi import HTTPException

def get_research_question_mapping(db: Session, research_question_mapping_id: int):
    mapping = db.query(ResearchQuestionMapping).filter(ResearchQuestionMapping.research_question_mapping_id == research_question_mapping_id).first()
    if not mapping:
        raise HTTPException(status_code=404, detail="Research question mapping not found")
    return mapping

def get_research_question_mappings(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ResearchQuestionMapping).offset(skip).limit(limit).all()

def create_research_question_mapping(db: Session, research_question_mapping: ResearchQuestionMappingCreate):
    db_research_question_mapping = ResearchQuestionMapping(**research_question_mapping.dict())
    db.add(db_research_question_mapping)
    db.commit()
    db.refresh(db_research_question_mapping)
    return db_research_question_mapping

def update_research_question_mapping(db: Session, research_question_mapping_id: int, research_question_mapping: ResearchQuestionMappingUpdate):
    db_research_question_mapping = db.query(ResearchQuestionMapping).filter(ResearchQuestionMapping.research_question_mapping_id == research_question_mapping_id).first()
    if not db_research_question_mapping:
        raise HTTPException(status_code=404, detail="Research question mapping not found")
    for key, value in research_question_mapping.dict(exclude_unset=True).items():
        setattr(db_research_question_mapping, key, value)
    db.commit()
    db.refresh(db_research_question_mapping)
    return db_research_question_mapping

def delete_research_question_mapping(db: Session, research_question_mapping_id: int):
    mapping = db.query(ResearchQuestionMapping).filter(ResearchQuestionMapping.research_question_mapping_id == research_question_mapping_id).first()
    if not mapping:
        raise HTTPException(status_code=404, detail="Research question mapping not found")
    db.delete(mapping)
    db.commit()
    return mapping