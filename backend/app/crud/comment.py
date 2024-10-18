# app/crud/comment.py
from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate
from fastapi import HTTPException

def get_comment(db: Session, comment_id: int):
    comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

def update_comment(db: Session, comment_id: int, comment: CommentUpdate):
    db_comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if not db_comment:
        return None
    for key, value in comment.dict(exclude_unset=True).items():
        setattr(db_comment, key, value)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if not db_comment:
        return None
    db.delete(db_comment)
    db.commit()
    return db_comment

def get_comments_by_article(db: Session, article_id: int):
    return db.query(Comment).filter(Comment.article_id == article_id).all()

def create_comment(db: Session, article_id: int, comment: CommentCreate, user_id: int):
    db_comment = Comment(
        article_id=article_id,
        user_id=user_id,
        comment_text=comment.comment_text
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment