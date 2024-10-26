# app/schemas/collaboration.py
from pydantic import BaseModel
from datetime import datetime


class CollaborationBase(BaseModel):
    article_id: int
    user_id: int


class CollaborationCreate(CollaborationBase):
    pass


class CollaborationRead(CollaborationBase):
    collaboration_id: int
    created_at: datetime

    class Config:
        orm_mode = True
