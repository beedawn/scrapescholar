# app/schemas/searchkeyword.py
from pydantic import BaseModel

class SearchKeywordBase(BaseModel):
    search_id: int
    keyword_id: int

class SearchKeywordCreate(SearchKeywordBase):
    pass

class SearchKeywordRead(SearchKeywordBase):
    search_keyword_id: int

    class Config:
        orm_mode = True