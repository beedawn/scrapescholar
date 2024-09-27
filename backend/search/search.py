# search/search.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.search import Search
from app.models.user import User
from fastapi_login import LoginManager
from auth.auth import login_manager

router = APIRouter()

# Helper function to get the logged-in user
@login_manager.user_loader
def get_current_user(db: Session = Depends(get_db)):
    return login_manager.get_current_user()  # Fetches the user data from the access token

@router.get("/user/searches", status_code=status.HTTP_200_OK)
def get_last_300_searches(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve the last 300 searches for the logged-in user.
    """
    # Query the last 300 searches for the authenticated user
    searches = (
        db.query(Search)
        .filter(Search.user_id == current_user.user_id)
        .order_by(Search.search_date.desc())
        .limit(300)
        .all()
    )

    # Return the list of searches (empty list if none found)
    return searches