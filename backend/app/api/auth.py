# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserLogin
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
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Load user by email for login manager
@login_manager.user_loader
def load_user(email: str, db: Session = Depends(get_db)):
    return db.query(User).filter(User.email == email).first()

# Login route: allow both email and username for login
@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # First try to find user by email
    user = db.query(User).filter(User.email == data.username).first()

    # If not found by email, try finding by username
    if not user:
        user = db.query(User).filter(User.username == data.username).first()

    # If user is still not found or the password is incorrect
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or username, or password"
        )

    # Create access token using the user's email
    access_token = login_manager.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
