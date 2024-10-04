# app/schemas/search.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SearchBase(BaseModel):
    search_keywords: Optional[List[str]] = None
    status: Optional[str] = "active"
    title: str

class SearchCreate(SearchBase):
    pass

class SearchUpdate(BaseModel):
    search_keywords: Optional[List[str]] = None
    status: Optional[str] = None

class SearchRead(SearchBase):
    search_id: int
    search_date: datetime
    user_id: int  # This will be used when reading the search information

    class Config:
        orm_mode = True