# endpoints/comment/comment.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.crud.comment import create_comment, update_comment, delete_comment, get_comments_by_article, get_comment
from app.schemas.comment import CommentCreate, CommentUpdate, Comment
from app.db.session import get_db

router = APIRouter()

# Add a comment to an article
@router.post("/articles/{article_id}/comments", response_model=Comment)
def create_new_comment(article_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    new_comment = create_comment(db, article_id=article_id, comment=comment)
    return new_comment

# Edit a comment
@router.put("/comments/{comment_id}", response_model=Comment)
def update_existing_comment(comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db)):
    existing_comment = get_comment(db, comment_id=comment_id)
    if existing_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    updated_comment = update_comment(db, comment_id=comment_id, comment=comment)
    return updated_comment

# Delete a comment
@router.delete("/comments/{comment_id}")
def remove_comment(comment_id: int, db: Session = Depends(get_db)):
    existing_comment = get_comment(db, comment_id=comment_id)
    if existing_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    delete_comment(db, comment_id=comment_id)
    return {"detail": "Comment deleted successfully"}

# Get all comments for an article
@router.get("/articles/{article_id}/comments", response_model=List[Comment])
def get_comments(article_id: int, db: Session = Depends(get_db)):
    comments = get_comments_by_article(db, article_id=article_id)
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for this article")
    return comments