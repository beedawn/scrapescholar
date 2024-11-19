# app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException, status
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
from app.crud.article import delete_article_by_user_id

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
load_dotenv()
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")  # Store this securely!
fernet = Fernet(ENCRYPTION_KEY)


def hash(text: str) -> str:
    return pwd_context.hash(text)


def verify_hash(text: str, hashed_text: str) -> bool:
    return pwd_context.verify(text, hashed_text)


def encrypt(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()


def decrypt(encrypted_text: str) -> str:
    return fernet.decrypt(encrypted_text.encode()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_all_users(db: Session):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    decrypted_usernames = []
    for user in users:
        decrypt_username = decrypt(user.username)
        decrypted_user = {"username": decrypt_username,
                          "user_id": user.user_id,
                          "role_id": user.role_id,
                          }
        decrypted_usernames.append(decrypted_user)
    return decrypted_usernames


def get_user_by_username(db: Session, username: str):
    encrypted_username = encrypt(username)
    users = db.query(User).all()
    for user in users:
        plaintext_user = decrypt(user.username)
        if plaintext_user == username:
            return user
    return None


def get_user_by_email(db: Session, email: str):
    hashed_emails = db.query(User).all()
    for hashed_email in hashed_emails:
        if verify_hash(email, hashed_email.email):
            return hashed_email
    return False


def create_user(db: Session, user: UserCreate):
    hashed_password = hash(user.password)
    encrypted_username = encrypt(user.username)
    if db.query(User).filter(User.username == encrypted_username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    if user.email is not None:
        hashed_email = hash(user.email)
        if db.query(User).filter(User.email == hashed_email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        db_user = User(
            username=encrypted_username,
            email=hashed_email,
            password=hashed_password,
            role_id=user.role_id
        )
    else:
        db_user = User(
            username=encrypted_username,
            password=hashed_password,
            role_id=user.role_id
        )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password:
        user.password = hash(user.password)
    if user.username:
        user.username = encrypt(user.username)
    if user.email:
        user.email = hash(user.email)
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    delete_article_by_user_id(db, user_id)
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user
