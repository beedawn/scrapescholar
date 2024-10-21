# utils/auth.py
import jwt
from fastapi import Depends, HTTPException, status, Header, Cookie
from sqlalchemy.orm import Session
from app.db.session import get_db 
from app.models.user import User
import os
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("SECRET_KEY")
DEBUG_SCRAPESCHOLAR = os.getenv("DEBUG_SCRAPESCHOLAR", "FALSE").upper() == "TRUE"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Helper function to extract token from either cookie or Authorization header
async def get_token_from_cookie_or_header(access_token: str = Cookie(None), authorization: str = Header(None)):
    if authorization:
        token = authorization.split(" ")[1]  # Extract token from "Bearer {token}"
    elif access_token:
        token = access_token  # Use token from the cookie
    else:
        raise HTTPException(status_code=401, detail="Authorization token missing")
    return token

async def get_current_user(db: Session = Depends(get_db), access_token: str = Cookie(None), authorization: str = Header(None)):
    token = await get_token_from_cookie_or_header(access_token, authorization)
    
    try:
        if DEBUG_SCRAPESCHOLAR:
            print(f"Decoding token: {token}")

        # Decode the JWT token
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token payload does not contain a user ID",
            )

        if DEBUG_SCRAPESCHOLAR:
            print(f"User ID from token: {user_id}")

        # Query the user from the database
        user = db.query(User).filter(User.user_id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        if DEBUG_SCRAPESCHOLAR:
            print(f"Current user fetched: {user}")
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    except Exception as e:
        if DEBUG_SCRAPESCHOLAR:
            print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching the current user",
        )