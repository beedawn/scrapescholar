# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional, Union


class UserDataBase(BaseModel):
    userdata_id: int
    user_id: int
    article_id: int
    relevancy_color: str
    methodology: int
    clarity: int
    transparency: int
    completeness: int
    evaluation_criteria: Optional[str] = None


class UserDataCreate(UserDataBase):
    pass


class UserDataUpdate(BaseModel):
    article_id: int
    relevancy_color: Optional[str] = None
    methodology: Optional[Union[str, int]] = None
    clarity: Optional[Union[str, int]] = None
    transparency: Optional[Union[str, int]] = None
    completeness: Optional[Union[str, int]] = None
    evaluation_criteria: Optional[str] = None


class UserDataRead(UserDataBase):
    class Config:
        orm_mode = True
