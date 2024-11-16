# app/schemas/article.py
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import date


class ArticleBase(BaseModel):
    source_id: int
    title: str
    date: date
    link: Optional[HttpUrl] = None
    relevance_score: Optional[float] = None

    abstract: Optional[str] = None
    doi: Optional[str] = None
    document_type: Optional[str] = None
    citedby: Optional[int] = None


class ArticleCreate(ArticleBase):
    search_id: int


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    publication_date: Optional[date] = None
    journal: Optional[str] = None
    url: Optional[HttpUrl] = None
    relevance_score: Optional[float] = None
    review_status: Optional[str] = None
    abstract: Optional[str] = None
    doi: Optional[str] = None
    user_id: Optional[int] = None


class ArticleRead(ArticleBase):
    article_id: int
    user_id: int

    class Config:
        orm_mode = True

class Article(ArticleRead):
    pass