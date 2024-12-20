from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie, Request
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
from typing import Annotated
from datetime import timedelta
from auth_tools.is_admin import is_admin
from auth_tools.get_user import get_current_user_modular
from fastapi.responses import RedirectResponse

load_dotenv()

SECRET = os.getenv("SECRET_KEY")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
host_ip = os.getenv("HOST_IP")
fernet = Fernet(ENCRYPTION_KEY)
ENVIRONMENT = os.getenv("ENVIRONMENT")

if not SECRET:
    raise ValueError("SECRET_KEY environment variable is not set")

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

login_manager = LoginManager(SECRET, token_url="/auth/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()


def hash_string(text: str):
    return hash_context.hash(text)


def verify_hash(plain_text, hashed_text: str):
    return hash_context.verify(plain_text, hashed_text)


def encrypt_username(username: str) -> str:
    return fernet.encrypt(username.encode()).decode()


def decrypt_username(encrypted_username: str) -> str:
    try:
        return fernet.decrypt(encrypted_username.encode()).decode()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username")


@login_manager.user_loader
def load_user(user_id: str, db: Session = None):
    if db is None:
        db = next(get_db())
    return db.query(User).filter(User.user_id == int(user_id)).first()


@router.post("/login")
def login(request: Request=None, data: OAuth2PasswordRequestForm = Depends()):
    access_token = build_access_token(data.username, data.password)

    return cookie_response(access_token=access_token, request=request)


def build_access_token(username, password, azure_token=None):
    db: Session = SessionLocal()
    user = None
    for candidate in db.query(User).all():
        try:
            decrypted_username = decrypt_username(candidate.username)
            if decrypted_username == username:
                user = candidate
                break
            if verify_hash(username, candidate.email):
                user = candidate
                break
        except HTTPException:
            continue
    if not user and azure_token is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please contact your professor to create an account for you"
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username"
        )

    if not verify_hash(password, user.password) and azure_token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password"
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username"
        )

    access_token = login_manager.create_access_token(data={"sub": str(user.user_id)}, expires=timedelta(hours=8))
    return access_token


def cookie_response(access_token: str,  request: Request = None, azure_token=None,):
    content = {"access_token": access_token, "token_type": "bearer"}

    response = JSONResponse(content=content)
    if azure_token:
        scheme = request.url.scheme
        redirect_uri = f"{scheme}://{host_ip}/"
        print("ENVIRONMENT VARIABLE")
        print(ENVIRONMENT)
        if ENVIRONMENT is None or (ENVIRONMENT.lower() != "prod" and ENVIRONMENT.lower() != "production"):
            redirect_uri = f"{scheme}://{host_ip}:3000/"
        print("redirect uri")
        print(redirect_uri)
        response = RedirectResponse(url=redirect_uri)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        path="/",
        domain=f"{host_ip}",
        samesite="lax",
        max_age=28800
    )
    return response


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user_id = login_manager.get_user_id(token)
        user = load_user(user_id, db=db)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.get("/get_cookie")
async def get_cookie(access_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    user = get_current_user_modular(access_token, db)
    if access_token is None or user is None:
        raise HTTPException(status_code=404, detail="Cookie not found")
    return JSONResponse(content={"cookieValue": access_token})


@router.get("/is_admin")
async def is_admin_endpoint(access_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    get_current_user_modular(access_token, db)
    if is_admin(access_token, db):
        return True
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="")


@router.get("/remove_cookie")
def remove_cookie(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Cookie deleted"}
