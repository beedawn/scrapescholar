# endpoints/article/article.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.crud.article import create_article, get_article, delete_article
from app.schemas.article import ArticleCreate
from app.db.session import get_db

router = APIRouter()

# Get an article by ID
@router.get("/{article_id}")
def read_article(article_id: int, db: Session = Depends(get_db)):
    article = get_article(db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# Add a new article
@router.post("/")
def create_new_article(article: ArticleCreate, db: Session = Depends(get_db)):
    created_article = create_article(db, article)
    return created_article

# Delete an article by ID
@router.delete("/{article_id}")
def remove_article(article_id: int, db: Session = Depends(get_db)):
    article = get_article(db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    delete_article(db, article_id=article_id)
    return {"detail": "Article deleted successfully"}