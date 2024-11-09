# user/user.py

from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Query, Body
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.crud.user import create_user, get_user, get_user_by_username, update_user, delete_user, get_all_users, get_user_by_email
from app.models.role import Role
from app.db.session import get_db
from cryptography.fernet import Fernet
import os
from auth_tools.get_user import get_current_user_modular
from typing import List, Annotated
from dotenv import load_dotenv
from auth_tools.is_admin import is_admin
from pydantic import BaseModel


load_dotenv()

# Load environment variable for encryption key
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")


fernet = Fernet(ENCRYPTION_KEY)

router = APIRouter()


# Encrypt username helper function
def encrypt_username(username: str) -> str:
    return fernet.encrypt(username.encode()).decode()

# Define a schema for the request body
class RoleUpdateRequest(BaseModel):
    role_name: str

@router.put("/update-role/{user_id}", response_model=UserRead)
def update_user_role(
    user_id: int,
    role_request: RoleUpdateRequest,  # Use RoleUpdateRequest as the request body
    access_token: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db)
):
    current_user = get_current_user_modular(access_token, db)
    if not is_admin(access_token, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    # Fetch the role by role_name from the request body
    role = db.query(Role).filter(Role.role_name == role_request.role_name).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role not found.")

    user.role_id = role.role_id
    db.commit()
    db.refresh(user)
    return user


@router.post("/create", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate,access_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    """
    API endpoint to create a new user.
    """
    #probably want to verify user has valid token
    user_1 = get_current_user_modular(access_token, db)
    admin = is_admin(access_token, db)
    users = get_all_users(db)
    # Encrypt the username before checking for existence, probably need to decrypt db instead
    for useritem in users:
        if useritem["username"] == user.username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")
    # Check if the username already exists, needs work
    if admin:
        # Proceed with creating the user
        new_user = create_user(db=db, user=user)
        return new_user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="")

@router.get("/get/{user_id}", response_model=UserRead)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to get a user by their ID.
    """
    #probably want to verify user has valid token
    user = get_user(db=db, user_id=user_id)
    return user


@router.get("/get")
def get_users(access_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    """
    API endpoint to get a user by their ID.
    """
    #probably want to verify user has valid token
    get_current_user_modular(access_token, db)
    users = get_all_users(db)
    return users

@router.get("/get-by-username/{username}", response_model=UserRead)
def get_user_by_username_api(username: str, db: Session = Depends(get_db)):
    """
    API endpoint to get a user by their username.
    """
    #probably want to verify user has valid token

    # Encrypt the username before querying

    encrypted_username = encrypt_username(username)
    user = get_user_by_username(db=db, username=encrypted_username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


@router.put("/update/{user_id}", response_model=UserRead)
def update_existing_user(user_id: int,user: UserUpdate, access_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    """
    API endpoint to update an existing user.
    """
    #probably want to verify user has valid token
    get_current_user_modular(access_token, db)
    admin = is_admin(access_token, db)
    if admin:
        updated_user = update_user(db=db, user_id=user_id, user=user)
        return updated_user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="")


@router.delete("/delete/{user_id}", response_model=UserRead)
def delete_existing_user(user_id: int, access_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    """
    API endpoint to delete a user by their ID.
    """
    #probably want to verify user has valid token
    get_current_user_modular(access_token, db)
    admin = is_admin(access_token, db)
    if admin:
        deleted_user = delete_user(db=db, user_id=user_id)
        return deleted_user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="")