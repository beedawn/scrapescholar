# app/models/researchquestion.py
from sqlalchemy import Column, Integer, Text
from app.db.session import Base

class ResearchQuestion(Base):
    __tablename__ = "ResearchQuestion"

    research_question_id = Column(Integer, primary_key=True, index=True)
    research_question = Column(Text, nullable=False)