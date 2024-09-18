# app/crud/comment.py
from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.comment_id == comment_id).first()

def get_comments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Comment).offset(skip).limit(limit).all()

def create_comment(db: Session, comment: CommentCreate):
    db_comment = Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def update_comment(db: Session, comment_id: int, comment: CommentUpdate):
    db_comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if db_comment:
        for key, value in comment.dict(exclude_unset=True).items():
            setattr(db_comment, key, value)
        db.commit()
        db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment