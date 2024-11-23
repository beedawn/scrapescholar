from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommentCreate(BaseModel):
    comment_text: str


class CommentUpdate(BaseModel):
    comment_text: Optional[str] = None


class Comment(BaseModel):
    comment_id: int
    article_id: int
    user_id: int
    comment_text: str
    created_at: datetime

    class Config:
        orm_mode = True
