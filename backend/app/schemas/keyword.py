# app/schemas/keyword.py
from pydantic import BaseModel

class KeywordBase(BaseModel):
    keyword: str

class KeywordCreate(KeywordBase):
    pass

class KeywordUpdate(BaseModel):
    keyword: Optional[str] = None

class KeywordRead(KeywordBase):
    keyword_id: int

    class Config:
        orm_mode = True