# app/schemas/comment.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentBase(BaseModel):
    article_id: int
    user_id: int
    comment_text: Optional[str] = None

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    comment_text: Optional[str] = None

class CommentRead(CommentBase):
    comment_id: int
    created_at: datetime

    class Config:
        orm_mode = True