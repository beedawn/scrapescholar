# app/crud/articlescore.py
from sqlalchemy.orm import Session
from app.models.articlescore import ArticleScore
from app.schemas.articlescore import ArticleScoreCreate, ArticleScoreUpdate
from fastapi import HTTPException


def get_article_score(db: Session, article_score_id: int):
    article_score = db.query(ArticleScore).filter(ArticleScore.article_score_id == article_score_id).first()
    if not article_score:
        raise HTTPException(status_code=404, detail="Article score not found")
    return article_score


def get_article_scores(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ArticleScore).offset(skip).limit(limit).all()


def create_article_score(db: Session, article_score: ArticleScoreCreate):
    db_article_score = ArticleScore(**article_score.dict())
    db.add(db_article_score)
    db.commit()
    db.refresh(db_article_score)
    return db_article_score


def update_article_score(db: Session, article_score_id: int, article_score: ArticleScoreUpdate):
    db_article_score = db.query(ArticleScore).filter(ArticleScore.article_score_id == article_score_id).first()
    if not db_article_score:
        raise HTTPException(status_code=404, detail="Article score not found")
    for key, value in article_score.dict(exclude_unset=True).items():
        setattr(db_article_score, key, value)
    db.commit()
    db.refresh(db_article_score)
    return db_article_score


def delete_article_score(db: Session, article_score_id: int):
    db_article_score = db.query(ArticleScore).filter(ArticleScore.article_score_id == article_score_id).first()
    if not db_article_score:
        raise HTTPException(status_code=404, detail="Article score not found")
    db.delete(db_article_score)
    db.commit()
    return db_article_score
