# endpoints/article/article.py
from fastapi import APIRouter, HTTPException, Depends, Cookie, Header
from sqlalchemy.orm import Session
from app.crud.article import create_article, get_article, delete_article, update_article
from app.schemas.article import ArticleCreate, ArticleUpdate, Article
from app.db.session import get_db
from utils.auth import get_current_user_no_route
from app.models.user import User

router = APIRouter()

# Helper function to extract token from either cookie or header
async def get_token_from_cookie_or_header(access_token: str = Cookie(None), authorization: str = Header(None)):
    if authorization:
        token = authorization.split(" ")[1]  # Extract token from "Bearer {token}"
    elif access_token:
        token = access_token  # Use token from the cookie
    else:
        raise HTTPException(status_code=401, detail="Authorization token missing")
    return token

# Get an article by ID
@router.get("/{article_id}", response_model=Article, status_code=200)
async def read_article(article_id: int, db: Session = Depends(get_db)):
    article = get_article(db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# Add a new article (works with both cookie and Authorization header)
@router.post("/", response_model=Article, status_code=201)
async def create_new_article(
    article: ArticleCreate, 
    db: Session = Depends(get_db),
    access_token: str = Cookie(None), 
    authorization: str = Header(None)
):
    token = await get_token_from_cookie_or_header(access_token, authorization)
    current_user = await get_current_user_no_route(token=token, db=db)

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    created_article = create_article(db, article, user_id=current_user.user_id)
    return created_article

# Update an article by ID (works with both cookie and Authorization header)
@router.put("/{article_id}", response_model=Article, status_code=200)
async def update_existing_article(
    article_id: int, 
    article: ArticleUpdate, 
    db: Session = Depends(get_db),
    access_token: str = Cookie(None), 
    authorization: str = Header(None)
):
    token = await get_token_from_cookie_or_header(access_token, authorization)
    current_user = await get_current_user_no_route(token=token, db=db)

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    existing_article = get_article(db, article_id=article_id)
    if existing_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if existing_article.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this article")

    updated_article = update_article(db, article_id, article)
    return updated_article

# Delete an article by ID (works with both cookie and Authorization header)
@router.delete("/{article_id}", status_code=204)
async def remove_article(
    article_id: int, 
    db: Session = Depends(get_db),
    access_token: str = Cookie(None), 
    authorization: str = Header(None)
):
    token = await get_token_from_cookie_or_header(access_token, authorization)
    current_user = await get_current_user_no_route(token=token, db=db)

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    article = get_article(db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this article")

    delete_article(db, article_id=article_id)
    return None

    if existing_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if existing_article.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this article")

    updated_article = update_article(db, article_id, article)
    return updated_article

# Delete an article by ID (requires user authentication)
@router.delete("/{article_id}", status_code=204)
async def remove_article(
    article_id: int, 
    db: Session = Depends(get_db),
    access_token: str = Cookie(None)
):
    current_user = await get_current_user_no_route(token=access_token, db=db)
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    article = get_article(db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this article")

    delete_article(db, article_id=article_id)
    return None