# app/schemas/user.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserLogin(BaseModel):
    username: str
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long.")


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long.")
    role_id: Optional[int] = 2  # Default role ID is 2 (regular user)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, description="Password must be at least 8 characters long.")
    role_id: Optional[int] = None


class UserRead(UserBase):
    user_id: int
    role_id: int
    registration_date: datetime

    class Config:
        orm_mode = True
