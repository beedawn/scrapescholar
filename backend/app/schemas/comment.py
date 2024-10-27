# app/schemas/comment.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema for creating a new comment
class CommentCreate(BaseModel):
    comment_text: str

# Schema for updating an existing comment
class CommentUpdate(BaseModel):
    comment_text: Optional[str] = None

# Schema for reading a comment (response model)
class Comment(BaseModel):
    comment_id: int
    article_id: int
    user_id: int
    comment_text: str
    created_at: datetime

    class Config:
        orm_mode = True
