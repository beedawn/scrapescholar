from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class ResearchQuestionMapping(Base):
    __tablename__ = "ResearchQuestionMapping"

    research_question_mapping_id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("Article.article_id"))
    research_question_id = Column(Integer, ForeignKey("ResearchQuestion.research_question_id"))

    article = relationship("Article", back_populates="research_question_mappings")
    research_question = relationship("ResearchQuestion", back_populates="research_question_mappings")
    research_question_scores = relationship("ResearchQuestionScore",
                                            back_populates="research_question_mapping")