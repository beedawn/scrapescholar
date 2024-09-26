# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserLogin(BaseModel):
    username: str
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long.")

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long.")

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, description="Password must be at least 8 characters long.")

class UserRead(UserBase):
    user_id: int
    role_id: int
    registration_date: datetime

    class Config:
        orm_mode = True