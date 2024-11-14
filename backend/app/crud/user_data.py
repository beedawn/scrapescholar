# app/crud/user_data.py
from sqlalchemy.orm import Session
from app.models.user_data import UserData
from app.models.role import Role
from app.schemas.user_data import UserDataCreate, UserDataUpdate
from fastapi import HTTPException
from auth_tools.is_admin import is_admin
import os


def get_user_data(db: Session, article_id: int):
    user_data = (db.query(UserData)
                 .filter(UserData.article_id == article_id)
                 .first())
    if not user_data:
        raise HTTPException(status_code=404, detail="Userdata not found in get")
    return user_data


def create_user_data(db: Session, user_id, article_id):
    db_user_data = UserData(
        user_id=user_id,
        article_id=article_id,
    )
    db.add(db_user_data)
    db.commit()
    db.refresh(db_user_data)
    return db_user_data


async def update_user_data(db: Session, user_data: UserDataUpdate, user_role: str, access_token):
    db_user_data = db.query(UserData).filter(UserData.article_id == user_data.article_id).first()
    if not db_user_data:
        raise HTTPException(status_code=404, detail="Userdata not found in put, user not valid in db")
    if not is_admin(access_token, db) and "evaluation_criteria" in user_data.dict(exclude_unset=True):
        raise HTTPException(status_code=403, detail="Only professors can edit evaluation criteria")
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(db_user_data, key, value)
    db.commit()
    db.refresh(db_user_data)
    return db_user_data


def delete_user_data(db: Session, userdata_id: int):
    db_userdata = db.query(UserData).filter(UserData.userdata_id == userdata_id).first()
    if not db_userdata:
        raise HTTPException(status_code=404, detail="Userdata not found")
    db.delete(db_userdata)
    db.commit()
    return db_userdata


def delete_user_data_by_article(db: Session, article_id: int):
    db_userdata = db.query(UserData).filter(UserData.article_id == article_id).first()
    if not db_userdata:
        raise HTTPException(status_code=404, detail="Userdata not found")
    db.delete(db_userdata)
    db.commit()
    return db_userdata


def delete_user_data_by_article_id(db: Session, article_id: int):
    user_data_entries = db.query(UserData).filter(UserData.article_id == article_id).all()
    for entry in user_data_entries:
        db.delete(entry)
    db.commit()
