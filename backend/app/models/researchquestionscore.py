# app/models/researchquestionscore.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class ResearchQuestionScore(Base):
    __tablename__ = "ResearchQuestionScore"

    research_question_score_id = Column(Integer, primary_key=True, index=True)
    research_question_mapping_id = Column(Integer, ForeignKey("ResearchQuestionMapping.research_question_mapping_id",
                                                              ondelete="CASCADE"))
    score = Column(Integer, nullable=False)
    last_updated_by_id = Column(Integer, ForeignKey("User.user_id"))

    research_question_mapping = relationship("ResearchQuestionMapping",
                                             back_populates="research_question_scores")  # Added back_populates
    last_updated_by = relationship("User", back_populates="research_question_scores")
