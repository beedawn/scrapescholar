# app/crud/comment.py
from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentUpdate
from fastapi import HTTPException
from datetime import datetime
from app.crud.user import decrypt


def parse_comment(new_comment: Comment, db:Session):
    found_username = db.query(User).filter(new_comment.user_id == User.user_id).first()
    decrypted_username = decrypt(found_username.username)

    new_comment_with_username = {
        "username": decrypted_username,
        "article_id": new_comment.article_id,
        "comment_id": new_comment.comment_id,
        "comment_text": new_comment.comment_text,
        "created_at": new_comment.created_at,
        "user_id": new_comment.user_id
    }
    return new_comment_with_username

def get_comment(db: Session, comment_id: int):
    comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


def get_comments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Comment).offset(skip).limit(limit).all()


def update_comment(db: Session, comment_id: int, comment: CommentUpdate):
    db_comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if not db_comment:
        return None
    for key, value in comment.dict(exclude_unset=True).items():
        setattr(db_comment, key, value)
    db.commit()
    db.refresh(db_comment)

    new_comment_with_username = parse_comment(db_comment, db)
    return new_comment_with_username


def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if not db_comment:
        return None
    db.delete(db_comment)
    db.commit()
    return db_comment


def get_comments_by_article(db: Session, article_id: int):
    comments = db.query(Comment).filter(Comment.article_id == article_id).all()
    return_array = []
    for comment in comments:
        found_username = db.query(User).filter(comment.user_id == User.user_id).first()
        decrypted_username = decrypt(found_username.username)
        return_array.append({
            "username": decrypted_username,
            "article_id": comment.article_id,
            "comment_id": comment.comment_id,
            "comment_text": comment.comment_text,
            "created_at": comment.created_at,
            "user_id": comment.user_id
        })
    return return_array


def create_comment(db: Session, article_id: int, comment: CommentCreate, user_id: int):
    new_comment = Comment(
        article_id=article_id,
        comment_text=comment.comment_text,
        user_id=user_id,
        created_at=datetime.utcnow()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    new_comment_with_username = parse_comment(new_comment, db)

    return new_comment_with_username
