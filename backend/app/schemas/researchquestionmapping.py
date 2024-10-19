# app/schemas/researchquestionmapping.py
from pydantic import BaseModel


class ResearchQuestionMappingBase(BaseModel):
    article_id: int
    research_question_id: int


class ResearchQuestionMappingCreate(ResearchQuestionMappingBase):
    pass


class ResearchQuestionMappingRead(ResearchQuestionMappingBase):
    research_question_mapping_id: int

    class Config:
        orm_mode = True
