# app/crud/researchquestionscore.py
from sqlalchemy.orm import Session
from app.models.researchquestionscore import ResearchQuestionScore
from app.schemas.researchquestionscore import ResearchQuestionScoreCreate, ResearchQuestionScoreUpdate

def get_research_question_score(db: Session, research_question_score_id: int):
    return db.query(ResearchQuestionScore).filter(ResearchQuestionScore.research_Question_Score_id == research_question_score_id).first()

def get_research_question_scores(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ResearchQuestionScore).offset(skip).limit(limit).all()

def create_research_question_score(db: Session, research_question_score: ResearchQuestionScoreCreate):
    db_research_question_score = ResearchQuestionScore(**research_question_score.dict())
    db.add(db_research_question_score)
    db.commit()
    db.refresh(db_research_question_score)
    return db_research_question_score

def update_research_question_score(db: Session, research_question_score_id: int, research_question_score: ResearchQuestionScoreUpdate):
    db_research_question_score = db.query(ResearchQuestionScore).filter(ResearchQuestionScore.research_Question_Score_id == research_question_score_id).first()
    if db_research_question_score:
        for key, value in research_question_score.dict(exclude_unset=True).items():
            setattr(db_research_question_score, key, value)
        db.commit()
        db.refresh(db_research_question_score)
    return db_research_question_score

def delete_research_question_score(db: Session, research_question_score_id: int):
    db_research_question_score = db.query(ResearchQuestionScore).filter(ResearchQuestionScore.research_Question_Score_id == research_question_score_id).first()
    if db_research_question_score:
        db.delete(db_research_question_score)
        db.commit()
    return db_research_question_score