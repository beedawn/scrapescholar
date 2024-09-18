# app/crud/researchquestionmapping.py
from sqlalchemy.orm import Session
from app.models.researchquestionmapping import ResearchQuestionMapping
from app.schemas.researchquestionmapping import ResearchQuestionMappingCreate, ResearchQuestionMappingUpdate

def get_research_question_mapping(db: Session, research_question_mapping_id: int):
    return db.query(ResearchQuestionMapping).filter(ResearchQuestionMapping.research_question_mapping_id == research_question_mapping_id).first()

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
    if db_research_question_mapping:
        for key, value in research_question_mapping.dict(exclude_unset=True).items():
            setattr(db_research_question_mapping, key, value)
        db.commit()
        db.refresh(db_research_question_mapping)
    return db_research_question_mapping

def delete_research_question_mapping(db: Session, research_question_mapping_id: int):
    db_research_question_mapping = db.query(ResearchQuestionMapping).filter(ResearchQuestionMapping.research_question_mapping_id == research_question_mapping_id).first()
    if db_research_question_mapping:
        db.delete(db_research_question_mapping)
        db.commit()
    return db_research_question_mapping