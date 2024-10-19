# app/schemas/source.py
from pydantic import BaseModel
from typing import Optional


class SourceBase(BaseModel):
    name: str
    api_endpoint: Optional[str] = None
    scrape_source_url: Optional[str] = None


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    name: Optional[str] = None
    api_endpoint: Optional[str] = None
    scrape_source_url: Optional[str] = None


class SourceRead(SourceBase):
    source_id: int

    class Config:
        orm_mode = True
