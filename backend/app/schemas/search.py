from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SearchBase(BaseModel):
    user_id: int
    search_keywords: Optional[List[str]] = None
    status: Optional[str] = "active"
    title: str


class SearchCreate(SearchBase):
    pass


class SearchUpdate(BaseModel):
    title: str
    status: Optional[str] = None


class SearchRead(SearchBase):
    search_id: int
    search_date: datetime
    user_id: int

    class Config:
        orm_mode = True
