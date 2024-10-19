# app/schemas/searchshare.py
from pydantic import BaseModel
from datetime import datetime


class SearchShareBase(BaseModel):
    search_id: int
    shared_with_user_id: int
    shared_by_user_id: int


class SearchShareCreate(SearchShareBase):
    pass


class SearchShareRead(SearchShareBase):
    share_id: int
    share_date: datetime

    class Config:
        orm_mode = True
