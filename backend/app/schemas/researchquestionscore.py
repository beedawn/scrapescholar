# app/schemas/researchquestionscore.py
from pydantic import BaseModel
from typing import Optional


class ResearchQuestionScoreBase(BaseModel):
    research_question_mapping_id: int
    score: int


class ResearchQuestionScoreCreate(ResearchQuestionScoreBase):
    pass


class ResearchQuestionScoreUpdate(BaseModel):
    score: Optional[int] = None


class ResearchQuestionScoreRead(ResearchQuestionScoreBase):
    research_question_score_id: int
    last_updated_by_id: int

    class Config:
        orm_mode = True
