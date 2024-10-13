# app/crud/user_data.py
from sqlalchemy.orm import Session
from app.models.user_data import UserData
from app.schemas.user_data import UserDataCreate, UserDataUpdate
from fastapi import HTTPException
import os

async def get_user_data(db: Session, article_id: int):
    print(f"Searching for UserData with article_id: {article_id}")
    user_data = (db.query(UserData)
                 .filter(UserData.article_id == article_id)
                 .first())
    if not user_data:
        raise HTTPException(status_code=404, detail="Userdata not found in get")
    return user_data

async def create_user_data(db: Session, user_id, article_id):
    db_user_data = UserData(
        user_id=user_id,
        article_id=article_id,
    )

    db.add(db_user_data)
    db.commit()
    db.refresh(db_user_data)
    return db_user_data

async def update_user_data(db: Session, user_data:UserData):
    db_user_data = db.query(UserData).filter(UserData.article_id == user_data.article_id).first()
    
    if not db_user_data:
        raise HTTPException(status_code=404, detail="Userdata not found in put")
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(db_user_data, key, value)
    db.commit()
    db.refresh(db_user_data)
    return db_user_data

# def delete_user(db: Session, user_id: int):
#     db_user = db.query(User).filter(User.user_id == user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")

#     db.delete(db_user)
#     db.commit()
#     return db_user