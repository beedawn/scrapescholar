# app/schemas/researchquestion.py
from pydantic import BaseModel


class ResearchQuestionBase(BaseModel):
    research_question: str


class ResearchQuestionCreate(ResearchQuestionBase):
    pass


class ResearchQuestionRead(ResearchQuestionBase):
    research_question_id: int

    class Config:
        orm_mode = True


class ResearchQuestionUpdate:
    pass