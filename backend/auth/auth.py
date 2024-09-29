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

# Load user by email for login manager
@login_manager.user_loader
def load_user(email: str, db: Session = Depends(get_db)):
    return db.query(User).filter(User.email == email).first()

# Login route: allow both email and username for login
@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    users = db.query(User).all()
    user = None
    for candidate in users:
        if(verify_hash(data.username, candidate.username)):
            user = candidate
    # First try to find user by email
    for candidate in users:
        print(data.username)
        print(candidate.email)
        print(verify_hash(data.username,candidate.email))
        if(verify_hash(data.username, candidate.email)):
            user = candidate

    #doesn't check email, 0auth has no email field?
    # user = db.query(User).filter(verify_hash(data.username,User.username)).first()
    print("USER:::::::::::")
    print(user)


    # If user is still not found or the password is incorrect
    if not user or not verify_hash(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or username, or password"
        )

    # Create access token using the user's email
    access_token = login_manager.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
