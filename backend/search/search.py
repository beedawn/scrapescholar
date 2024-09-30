# search/search.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.search import Search
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer
from app.crud.search import create_search
from app.schemas.search import SearchCreate
from app.schemas.article import ArticleCreate, ArticleBase
from app.crud.article import create_article
from pydantic import HttpUrl
import jwt  # Import JWT
from dotenv import load_dotenv
from typing import List
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


# Endpoint to save a requested search
@router.post("/user/searches", status_code=status.HTTP_200_OK)
async def post_search(search:SearchCreate, articles:List[ArticleBase], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Save a search to the DB
    """

    """
    todo: 
    check what searches the user has in history,
    generate an id based off the current searchs in history?
    add search and search ID
    can probably remove search from the parameters, as this will create the search, and possibly return it?
    get a list of articles from the api request, a search,
    save the search as a whole ie create a search, 
    then save each article within the DB ie create one to many articles
        and associate it the search

    is it better to have this as an endpoint or run this when the /academic_data end point is triggered?
    will leave as endpoint for now, its easier for testing/development
    """
    # create new search to associate articles to
    created_search = create_search(search=search, db=db)
    print("PRINTING SEARCH")
    print(search)
    print(type(search))
    print(articles)
    print(type(articles))

    print("PRINTING CREATED SEARCH")
    print(created_search)
    print(created_search.search_id)

    for article in articles:
        format_article= ArticleCreate(title=article.title,
        author=article.author,
        publication_date=article.publication_date,
        journal=article.journal,
        url=HttpUrl(article.url),
        relevance_score=article.relevance_score,
        review_status=article.review_status,
        abstract=article.abstract,
        doi=article.doi,
        source_id=article.source_id,
        search_id=created_search.search_id, 
        user_id=current_user.user_id)
        create_article(article=format_article, db=db)
    # try:
    #     # Query the last 300 searches for the authenticated user
    #     searches = (
    #         db.query(Search)
    #         .filter(Search.user_id == current_user.user_id)
    #         .order_by(Search.search_date.desc())
    #         .limit(300)
    #         .all()
    #     )
    #     return searches if searches else []

    # except Exception as e:
    #     if DEBUG_SCRAPESCHOLAR:
    #         print(f"Error retrieving searches: {str(e)}")
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving searches: {str(e)}")