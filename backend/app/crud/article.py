# app/crud/article.py
from sqlalchemy.orm import Session
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate

def get_article(db: Session, article_id: int):
    return db.query(Article).filter(Article.article_id == article_id).first()

def get_articles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Article).offset(skip).limit(limit).all()

def create_article(db: Session, article: ArticleCreate):
    db_article = Article(**article.dict(), user_id=user_id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def update_article(db: Session, article_id: int, article: ArticleUpdate):
    db_article = db.query(Article).filter(Article.article_id == article_id).first()
    if db_article:
        for key, value in article.dict(exclude_unset=True).items():
            setattr(db_article, key, value)
        db.commit()
        db.refresh(db_article)
    return db_article

def delete_article(db: Session, article_id: int):
    db_article = db.query(Article).filter(Article.article_id == article_id).first()
    if db_article:
        db.delete(db_article)
        db.commit()
    return db_article