# search/search.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.search import Search
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer
import jwt  # Import JWT
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the SECRET key from the environment
SECRET = os.getenv("SECRET_KEY")
DEBUG_SCRAPESCHOLAR = os.getenv("DEBUG_SCRAPESCHOLAR", "FALSE").upper() == "TRUE"

# Define OAuth2PasswordBearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter()

# Helper function to get the current user from token
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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

# Endpoint to retrieve the last 300 searches for the logged-in user
@router.get("/user/searches", status_code=status.HTTP_200_OK)
async def get_last_300_searches(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve the last 300 searches for the logged-in user.
    """
    try:
        # Query the last 300 searches for the authenticated user
        searches = (
            db.query(Search)
            .filter(Search.user_id == current_user.user_id)
            .order_by(Search.search_date.desc())
            .limit(300)
            .all()
        )
        return searches if searches else []

    except Exception as e:
        if DEBUG_SCRAPESCHOLAR:
            print(f"Error retrieving searches: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving searches: {str(e)}")