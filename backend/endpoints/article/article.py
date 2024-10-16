# endpoints/article/article.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.crud.article import create_article, get_article, delete_article, update_article
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.db.session import get_db
from utils.auth import get_current_user  # Import the auth utility
from app.models.user import User

router = APIRouter()

# Get an article by ID
@router.get("/{article_id}", status_code=200)
def read_article(article_id: int, db: Session = Depends(get_db)):
    article = get_article(db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# Add a new article (requires user authentication)
@router.post("/", status_code=201)
def create_new_article(article: ArticleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    created_article = create_article(db, article, user_id=current_user.user_id)
    return created_article

# Delete an article by ID (requires user authentication)
@router.delete("/{article_id}", status_code=204)
def remove_article(article_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    article = get_article(db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this article")
    delete_article(db, article_id=article_id)
    return None

@router.put("/{article_id}", status_code=200)
def update_existing_article(article_id: int, article: ArticleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_article = get_article(db, article_id=article_id)
    if existing_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if existing_article.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this article")
    updated_article = update_article(db, article_id, article)
    return updated_article