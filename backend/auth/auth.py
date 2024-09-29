# auth/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db, SessionLocal
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET = os.getenv("SECRET_KEY")

if not SECRET:
    raise ValueError("SECRET_KEY environment variable is not set")

# Password hashing context
hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Setup login manager
login_manager = LoginManager(SECRET, token_url="/auth/login")

# Create an API router for auth
router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Hash password
def hash(text: str):
    return hash_context.hash(text)

# Verify password
def verify_hash(plain_text, hashed_text: str):
    return hash_context.verify(plain_text, hashed_text)

# Register the user_loader callback with the login_manager
@login_manager.user_loader
def load_user(user_id: str, db: Session = None):
    if db is None:
        db = next(get_db())
    print(f"Loading user by user_id: {user_id}")
    return db.query(User).filter(User.user_id == int(user_id)).first()

# Login route
@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    users = db.query(User).all()
    user = None

    # Try to find user by username or email
    for candidate in users:
        if verify_hash(data.username, candidate.username):
            user = candidate
        elif verify_hash(data.username, candidate.email):
            user = candidate

    print(f"User found: ID={user.user_id}, Username={user.username}, Email={user.email}")

    if not user or not verify_hash(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or username, or password"
        )

    access_token = login_manager.create_access_token(data={"sub": str(user.user_id)})
    print(f"Access Token Generated: {access_token}")
    return {"access_token": access_token, "token_type": "bearer"}