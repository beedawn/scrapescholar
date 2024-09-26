# app/api/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.crud.user import create_user, get_user, get_user_by_username, update_user, delete_user
from app.db.session import get_db

router = APIRouter()

@router.post("/create", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    API endpoint to create a new user.
    """
    # Check if the username already exists
    try:
        existing_user = get_user_by_username(db, user.username)
    except HTTPException:
        existing_user = None

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")
    
    new_user = create_user(db=db, user=user)
    return new_user

@router.get("/get/{user_id}", response_model=UserRead)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to get a user by their ID.
    """
    user = get_user(db=db, user_id=user_id)
    return user

@router.get("/get-by-username/{username}", response_model=UserRead)
def get_user_by_username_api(username: str, db: Session = Depends(get_db)):
    """
    API endpoint to get a user by their username.
    """
    user = get_user_by_username(db=db, username=username)
    return user

@router.put("/update/{user_id}", response_model=UserRead)
def update_existing_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    API endpoint to update an existing user.
    """
    updated_user = update_user(db=db, user_id=user_id, user=user)
    return updated_user

@router.delete("/delete/{user_id}", response_model=UserRead)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to delete a user by their ID.
    """
    deleted_user = delete_user(db=db, user_id=user_id)
    return deleted_user