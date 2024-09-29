# search/search.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.search import Search
from app.models.user import User
from fastapi_login import LoginManager
from auth.auth import login_manager
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter()

# Helper function to get the current user from token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    print(f"Decoding token: {token}")
    user = login_manager.get_current_user(token)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or credentials")
    
    print(f"Current user fetched: {user}")
    return user

# Endpoint to retrieve the last 300 searches for the logged-in user
@router.get("/user/searches", status_code=status.HTTP_200_OK)
async def get_last_300_searches(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve the last 300 searches for the logged-in user.
    """
    try:
        searches = (
            db.query(Search)
            .filter(Search.user_id == current_user.user_id)
            .order_by(Search.search_date.desc())
            .limit(300)
            .all()
        )
        return searches if searches else []

    except Exception as e:
        print(f"Error retrieving searches: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving searches: {str(e)}")