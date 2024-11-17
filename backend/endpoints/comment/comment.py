# endpoints/comment/comment.py
from fastapi import APIRouter, HTTPException, Depends, Header, Cookie
from sqlalchemy.orm import Session
from typing import List
from app.crud.comment import create_comment, update_comment, delete_comment, get_comments_by_article, get_comment
from app.schemas.comment import CommentCreate, CommentUpdate, Comment
from app.db.session import get_db

from auth_tools.get_user import get_current_user_modular

router = APIRouter()


# Add a comment to an article
@router.post("/article/{article_id}", status_code=201)
async def create_new_comment(
        article_id: int,
        comment: CommentCreate,
        db: Session = Depends(get_db),
        access_token: str = Cookie(None)
):
    current_user = get_current_user_modular(db=db, token=access_token)

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    comments = get_comments_by_article(db, article_id=article_id)
    if len(comments) < 100:
        new_comment = create_comment(db, article_id=article_id, comment=comment, user_id=current_user.user_id)
    else:
        raise HTTPException(status_code=507, detail="Insufficient storage, article has 100 comments")

    return new_comment


# Edit a comment
@router.put("/{comment_id}")
async def update_existing_comment(
        comment_id: int,
        comment: CommentUpdate,
        db: Session = Depends(get_db),
        access_token: str = Cookie(None)

):
    current_user = get_current_user_modular(db=db, token=access_token)

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    existing_comment = get_comment(db, comment_id=comment_id)
    if existing_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if existing_comment.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to edit this comment")

    updated_comment = update_comment(db, comment_id=comment_id, comment=comment)
    return updated_comment


# Delete a comment
@router.delete("/{comment_id}", status_code=204)
async def remove_comment(
        comment_id: int,
        db: Session = Depends(get_db),
        access_token: str = Cookie(None),
        authorization: str = Header(None)
):
    current_user = get_current_user_modular(db=db, token=access_token)

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    existing_comment = get_comment(db, comment_id=comment_id)
    if existing_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if existing_comment.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this comment")

    delete_comment(db, comment_id=comment_id)
    return None


# Get all comments for an article
@router.get("/article/{article_id}/comments", status_code=200)
def get_comments(article_id: int, db: Session = Depends(get_db)):
    comments = get_comments_by_article(db, article_id=article_id)
    if comments:
        return comments
    return []
