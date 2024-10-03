# search/search.py
from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Query
from app.db.session import get_db
from app.models.search import Search
from app.models.article import Article
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer
from app.crud.search import create_search
from app.crud.user import decrypt
from app.schemas.search import SearchCreate
from app.schemas.article import ArticleCreate, ArticleBase
from app.crud.article import create_article
from pydantic import HttpUrl
import jwt  # Import JWT
from dotenv import load_dotenv
from typing import List, Annotated
import os
from datetime import datetime
from sqlalchemy.orm import Session



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
async def get_last_300_searches(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    """
    Retrieve the last 300 searches for the logged-in user.
    """
    current_user = await get_current_user_no_route(token=access_token, db=db)
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



# get single search and associated articles
@router.get("/user/articles", status_code=status.HTTP_200_OK)
async def get_search_articles(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None,  search_id: int = Query(None, description="ID of the specific search to retrieve")):
    """
    Retrieve a single search and asscoaited articles
    """
    current_user = await get_current_user_no_route(token=access_token, db=db)
    try:
        # Query the last 300 searches for the authenticated user
        search = (
            db.query(Search)
            .filter(Search.user_id == current_user.user_id, Search.search_id == search_id)
            .first()
        )

        articles = (
            db.query(Article)
            .filter(Article.search_id== search.search_id)
            .order_by(Article.title.desc())
            .all()
        )
        return articles if articles else []

    except Exception as e:
        if DEBUG_SCRAPESCHOLAR:
            print(f"Error retrieving search and associated articles: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving searches: {str(e)}")




async def post_search_no_route(keywords:List[str], articles:List[ArticleBase], db: Session , current_user: User ):
    """
    Save a search to the DB
    """

    """
    todo: 
    need to check if user has 300 searches, then respond with some kind of message to front end to let it know to bug them to delete searches
    """

    #check if there are 300 searches if there are, bail
    existing_searches = (
            db.query(Search)
            .filter(Search.user_id == current_user.user_id)
            .order_by(Search.search_date.desc())
            .limit(300)
            .all()
        )
    if (len(existing_searches)>=300):
        return False
    #title, date and user_id could this be better?
    decrypt_username=decrypt(current_user.username)
    title=f"{decrypt_username}-{datetime.now()}"
    # create new search to associate articles to
    search = SearchCreate(user_id=current_user.user_id, search_keywords=keywords,title=title)
    created_search = create_search(search=search, db=db, )

    # Define the format
    date_format = "%Y-%m-%d"
   
    for article in articles:
        format_article= ArticleCreate(
        title=article.title,
        date=datetime.strptime(article.date, date_format).date(),
        link=HttpUrl(article.link),
        relevance_score=article.relevance_score,
        evaluation_criteria=article.evaluation_criteria,
        abstract=article.abstract,
        citedby=article.citedby,
        document_type=article.document_type,
        #needs changed to something real
        source_id=1,
        search_id=created_search.search_id, 
        user_id=current_user.user_id)
        create_article(article=format_article, db=db)
  
    return True





async def get_current_user_no_route(db: Session, token: str = Depends(oauth2_scheme)):
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
