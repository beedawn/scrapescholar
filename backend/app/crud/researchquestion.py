# app/crud/researchquestion.py
from sqlalchemy.orm import Session
from app.models.researchquestion import ResearchQuestion
from app.schemas.researchquestion import ResearchQuestionCreate, ResearchQuestionUpdate

def get_research_question(db: Session, research_question_id: int):
    return db.query(ResearchQuestion).filter(ResearchQuestion.research_question_id == research_question_id).first()

def get_research_questions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ResearchQuestion).offset(skip).limit(limit).all()

def create_research_question(db: Session, research_question: ResearchQuestionCreate):
    db_research_question = ResearchQuestion(**research_question.dict())
    db.add(db_research_question)
    db.commit()
    db.refresh(db_research_question)
    return db_research_question

def update_research_question(db: Session, research_question_id: int, research_question: ResearchQuestionUpdate):
    db_research_question = db.query(ResearchQuestion).filter(ResearchQuestion.research_question_id == research_question_id).first()
    if db_research_question:
        for key, value in research_question.dict(exclude_unset=True).items():
            setattr(db_research_question, key, value)
        db.commit()
        db.refresh(db_research_question)
    return db_research_question

def delete_research_question(db: Session, research_question_id: int):
    db_research_question = db.query(ResearchQuestion).filter(ResearchQuestion.research_question_id == research_question_id).first()
    if db_research_question:
        db.delete(db_research_question)
        db.commit()
    return db_research_question
