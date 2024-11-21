# endpoints/article/article.py
from fastapi import APIRouter, HTTPException, Depends, Cookie
from sqlalchemy.orm import Session
from app.crud.article import create_article, get_article, delete_article, update_article
from app.schemas.article import ArticleCreate, ArticleUpdate, Article, ArticleRead
from app.db.session import get_db
from typing import Annotated
from auth_tools.get_user import get_current_user_modular
from app.crud.user_data import create_user_data, delete_user_data, get_user_data, update_user_data
from app.crud.search import get_search
from algorithm.algorithm_interface import algorithm_interface

router = APIRouter()


# Get an article by ID
@router.get("/{article_id}", response_model=Article, status_code=200)
async def read_article(article_id: int, access_token: Annotated[str | None, Cookie()] = None,
                       db: Session = Depends(get_db)):
    get_current_user_modular(access_token, db)
    article = get_article(db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


# Add a new article (authentication via token or cookie)
@router.post("/", response_model=ArticleRead, status_code=201)
async def create_new_article(
        article: ArticleCreate,
        access_token: Annotated[str | None, Cookie()] = None,
        db: Session = Depends(get_db)
):
    current_user = get_current_user_modular(access_token, db)
    search = get_search(db, article.search_id)
    relevance_score = algorithm_interface(" ".join(search.search_keywords), article.title, article.abstract)

    article_data = article.__dict__.copy()
    article_data.pop("relevance_score", None)
    article_with_relevance_score = ArticleCreate(**article_data, relevance_score=relevance_score)

    created_article = create_article(db, article_with_relevance_score, user_id=current_user.user_id)
    create_user_data(db, current_user.user_id, created_article.article_id)
    return created_article


@router.put("/{article_id}", response_model=Article, status_code=200)
async def update_existing_article(
        article_id: int,
        article: ArticleUpdate,
        access_token: Annotated[str | None, Cookie()] = None,
        db: Session = Depends(get_db)
):
    current_user = get_current_user_modular(access_token, db)
    existing_article = get_article(db, article_id=article_id)
    if existing_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if existing_article.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this article")

    updated_article = update_article(db, article_id, article)
    return updated_article


@router.delete("/{article_id}", status_code=204)
async def remove_article(
        article_id: int,
        db: Session = Depends(get_db),
        access_token: Annotated[str | None, Cookie()] = None

):
    current_user = get_current_user_modular(access_token, db)
    article = get_article(db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")

    if article.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this article")

    user_data = get_user_data(db, article.article_id)
    delete_user_data(db, user_data.userdata_id)
    delete_article(db, article_id=article_id)
    return None
