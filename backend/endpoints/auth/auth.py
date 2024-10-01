# auth/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.db.session import get_db, SessionLocal
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
from fastapi.responses import JSONResponse

load_dotenv()

SECRET = os.getenv("SECRET_KEY")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
fernet = Fernet(ENCRYPTION_KEY)

DEBUG_SCRAPESCHOLAR = os.getenv("DEBUG_SCRAPESCHOLAR", "FALSE").upper() == "TRUE"

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

# Encrypt username
def encrypt_username(username: str) -> str:
    return fernet.encrypt(username.encode()).decode()

# Decrypt username
def decrypt_username(encrypted_username: str) -> str:
    try:
        return fernet.decrypt(encrypted_username.encode()).decode()
    except Exception as e:
        if DEBUG_SCRAPESCHOLAR:
            print(f"Decryption failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username")

# Register the user_loader callback with the login_manager
@login_manager.user_loader
def load_user(user_id: str, db: Session = None):
    if db is None:
        db = next(get_db())
    if DEBUG_SCRAPESCHOLAR:
        print(f"Loading user by user_id: {user_id}")
    return db.query(User).filter(User.user_id == int(user_id)).first()

# Login route
@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db) ):

    # Iterate through all users and decrypt their usernames for comparison
    user = None
    for candidate in db.query(User).all():
        try:
            decrypted_username = decrypt_username(candidate.username)
            if decrypted_username == data.username:
                user = candidate
                break
        except HTTPException:
            continue  # Skip if decryption fails
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username"
        )

    # Ensure that the password matches
    if not verify_hash(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password"
        )

    if DEBUG_SCRAPESCHOLAR:
        print(f"User found: ID={user.user_id}, Username={user.username}, Email={user.email}")

    access_token = login_manager.create_access_token(data={"sub": str(user.user_id)})
    if DEBUG_SCRAPESCHOLAR:
        print(f"Access Token Generated: {access_token}")

    content = {"access_token": access_token, "token_type": "bearer"}
    response = JSONResponse(content=content)
    # will need to change this to secure for deployment
    response.set_cookie(
    key="access_token", 
    value=access_token, 
    httponly=True, 
    secure=False,
    path="/",
    domain="0.0.0.0",
    samesite="Lax",
    max_age=3600)

    return response


