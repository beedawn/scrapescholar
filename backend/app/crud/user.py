# app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException, status
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()
# Encryption key
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")  # Store this securely!
fernet = Fernet(ENCRYPTION_KEY)


# Helper function to hash fields
def hash(text: str) -> str:
    return pwd_context.hash(text)


def verify_hash(text: str, hashed_text: str) -> bool:
    return pwd_context.verify(text, hashed_text)


# Helper function to encrypt fields
def encrypt(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()


# Helper function to decrypt fields
def decrypt(encrypted_text: str) -> str:
    return fernet.decrypt(encrypted_text.encode()).decode()


# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_username(db: Session, username: str):
    #i dont think this works
    encrypted_username = encrypt(username)
    print("ENCRYPTED USERNAME")
    print(encrypted_username)
    #should we get all users, decrypt them, then compare? hmm

    users = db.query(User).all()
    for user in users:
        plaintext_user = decrypt(user.username)
        print(plaintext_user)
        if plaintext_user == username:
            return user
    user = db.query(User).filter(User.username == encrypted_username).first()

    return None



def get_user_by_email(db: Session, email: str):
    hashed_emails = db.query(User).all()
    for hashed_email in hashed_emails:
        print("ASHED EMAIL")
        print(hashed_email.email)
        if verify_hash(email, hashed_email.email):
            return hashed_email
    return False


def create_user(db: Session, user: UserCreate):
    # Hash the user's password and email, and encrypt the username before storing them
    hashed_password = hash(user.password)
    encrypted_username = encrypt(user.username)
    # not sure if these actually work might need to decrypt
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
    # i think we need to get the actual user from the db so it has an associated ID
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
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user
