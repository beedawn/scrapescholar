# app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user_data import UserData
from app.schemas.user_data import UserDataCreate, UserDataUpdate
from fastapi import HTTPException
from passlib.context import CryptContext
from cryptography.fernet import Fernet

from app.crud.user import get_user
import os





# def get_user_data(db: Session, user_id: int):
#     user = db.query(User).filter(User.user_id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

def create_user_data(db: Session, user_id, article_id):
    # Hash the user's password and email, and encrypt the username before storing them
    #get users user id

    #get article id

    db_user_data = UserData(
        user_id=user_id,
        article_id=article_id,
    )

    db.add(db_user_data)
    db.commit()
    db.refresh(db_user_data)
    return db_user_data

# def update_user_data(db: Session, user_id: int, user: UserUpdate):
#     db_user = db.query(User).filter(User.user_id == user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if user.password:
#         user.password = hash(user.password)

#     if user.username:
#         user.username = encrypt(user.username)

#     if user.email:
#         user.email = hash(user.email)

#     for key, value in user.dict(exclude_unset=True).items():
#         setattr(db_user, key, value)

#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def delete_user(db: Session, user_id: int):
#     db_user = db.query(User).filter(User.user_id == user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")

#     db.delete(db_user)
#     db.commit()
#     return db_user