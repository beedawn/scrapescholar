# app/schemas/articlescore.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ArticleScoreBase(BaseModel):
    user_id: int
    article_id: int
    score: float


class ArticleScoreCreate(ArticleScoreBase):
    pass


class ArticleScoreUpdate(BaseModel):
    score: Optional[float] = None


class ArticleScoreRead(ArticleScoreBase):
    article_score_id: int
    evaluation_date: datetime
    last_updated_at: datetime

    class Config:
        orm_mode = True
