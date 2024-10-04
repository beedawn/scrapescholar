# search/search.py
from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Query, Body
from app.db.session import get_db
from app.models.search import Search
from app.models.article import Article
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer
from app.crud.search import create_search

from app.crud.user import decrypt
from app.schemas.search import SearchCreate, SearchUpdate
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
    print("CURRENT USER")
    print(current_user)
    try:
        # Query the last 300 searches for the authenticated user
        searches = await get_300_search(db=db, current_user=current_user)
        print(searches)
        return searches if searches else []

    except Exception as e:
        if DEBUG_SCRAPESCHOLAR:
            print(f"Error retrieving searches: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving searches: {str(e)}")

# get single search and associated articles
@router.get("/user/articles", status_code=status.HTTP_200_OK)
async def get_search_articles(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None,  search_id: int = Query(None, description="ID of the specific search to retrieve")):
    """
    Retrieve a single search and associated articles
    """
    current_user = await get_current_user_no_route(token=access_token, db=db)
    try:
        # Query for the search
        search = await find_search(db=db, current_user=current_user,search_id=search_id)
   
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

# Add POST route to create a new search
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_new_search(
    search_data: SearchCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Create a new search and associate articles with it.
    """
    # Set the user_id from the current_user object
    search = Search(
        user_id=current_user.user_id,
        search_keywords=search_data.search_keywords,
        title=search_data.title,
        status=search_data.status,
        search_date=datetime.utcnow()
    )
    
    db.add(search)
    db.commit()
    db.refresh(search)
    
    return {"search_id": search.search_id}

# Retrieve a specific search by its ID
@router.get("/searchbyid/{search_id}", status_code=status.HTTP_200_OK)
async def get_search_by_id(search_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print(f"Fetching search for search_id: {search_id}, user_id: {current_user.user_id}")
    try:
        search = db.query(Search).filter(Search.user_id == current_user.user_id, Search.search_id == search_id).first()

        if not search:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Search not found")

        return search
    except Exception as e:
        if DEBUG_SCRAPESCHOLAR:
            print(f"Error retrieving search: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving search: {str(e)}")
# get single search and associated articles
@router.get("/user/search/title", status_code=status.HTTP_200_OK)
async def get_search_title(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None,  search_id: int = Query(None, description="ID of the specific search to retrieve")):
    """
    Retrieve a single search and associtated articles
    """
    current_user = await get_current_user_no_route(token=access_token, db=db)
    try:
        # Find the search
        search = await find_search(db=db, current_user=current_user,search_id=search_id)
        return {'title':search.title, 'keywords':search.search_keywords} if search else []

    except Exception as e:
        if DEBUG_SCRAPESCHOLAR:
            print(f"Error retrieving search and associated search: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving searches: {str(e)}")

# get single search and associated articles
@router.put("/user/search/title", status_code=status.HTTP_200_OK)
async def get_search_title(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None,  search_id: int = Query(None, description="ID of the specific search to retrieve"), search_data: SearchUpdate = Body(...)):
    """
    Update the title of an existing search
    """
    current_user = await get_current_user_no_route(token=access_token, db=db)
    try:
        # Query the last 300 searches for the authenticated user
        search = await find_search(db=db, current_user=current_user,search_id=search_id)
        search.title = search_data.title
        db.commit()
        db.refresh(search) 
        return search if search else []

    except Exception as e:
        if DEBUG_SCRAPESCHOLAR:
            print(f"Error retrieving search and associated search: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving searches: {str(e)}")

async def find_search(db,current_user,search_id):
    return  (
            db.query(Search)
            .filter(Search.user_id == current_user.user_id, Search.search_id == search_id)
            .first()
        )
async def get_300_search(db, current_user):
    return (
            db.query(Search)
            .filter(Search.user_id == current_user.user_id)
            .order_by(Search.search_date.desc())
            .limit(300)
            .all()
        )

async def check_if_user_exceeded_search_amount (db: Session , current_user: User ):
    #check if there are 300 searches if there are return true
    existing_searches = await get_300_search(db=db, current_user=current_user)
    if (len(existing_searches)>=300):
        print("amount exceeded!")
        return True
    else:
        print("amount not exceeded")
        return False

async def post_search_no_route(keywords:List[str], articles:List[ArticleBase], db: Session , current_user: User ):
    """
    Save a search to the DB
    """

    """
    todo: 
    need to check if user has 300 searches, then respond with some kind of message to front end to let it know to bug them to delete searches
    """


    result= await check_if_user_exceeded_search_amount(db, current_user)


    if result:
        return False, None

    #title, date and user_id could this be better?
    decrypt_username=decrypt(current_user.username)
    title=f"{decrypt_username}-{datetime.now()}"
    # create new search to associate articles to
    search = SearchCreate(user_id=current_user.user_id, search_keywords=keywords,title=title)
    #add loop for 300 search here
    x=0
    while x<300:
        created_search = create_search(search=search, db=db)
        x += 1

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
    
    return True, created_search.search_id


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
