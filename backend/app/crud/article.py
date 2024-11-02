# app/crud/article.py
from sqlalchemy.orm import Session
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate
from fastapi import HTTPException


def get_article(db: Session, article_id: int):
    article = db.query(Article).filter(Article.article_id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# app/crud/article.py
def get_articles(db: Session, skip: int = 0, limit: int = 10):
    # Ordering by `article_id` to ensure consistent results
    return db.query(Article).order_by(Article.article_id).offset(skip).limit(limit).all()

def create_article(db: Session, article: ArticleCreate, user_id: int):
    #db_article = Article(**article.dict())
    db_article = Article(
        source_id=article.source_id,
        search_id=article.search_id,
        title=article.title,
        date=article.date,
        link=str(article.link) if article.link else None,  # Convert to string
        relevance_score=article.relevance_score,
        abstract=article.abstract,
        citedby=article.citedby,
        document_type=article.document_type,
        doi=article.doi,
        user_id=user_id
    )

    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(db: Session, article_id: int, article: ArticleUpdate):
    db_article = db.query(Article).filter(Article.article_id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    for key, value in article.dict(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article


def delete_article(db: Session, article_id: int):
    db_article = db.query(Article).filter(Article.article_id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(db_article)
    db.commit()
    return db_article
