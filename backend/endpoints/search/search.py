# search/search.py
from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Query, Body
from app.db.session import get_db
from app.models.search import Search
from app.models.article import Article
from app.models.user import User
from app.models.user_data import UserData
from fastapi.security import OAuth2PasswordBearer
from app.crud.search import create_search
from app.crud.source import get_source_by_name, get_source
from app.crud.user import decrypt
from app.schemas.search import SearchCreate, SearchUpdate
from app.schemas.article import ArticleCreate, ArticleBase
from app.crud.article import create_article
from app.crud.user_data import create_user_data, get_user_data
from academic_databases.SearchResult import SearchResult
from pydantic import HttpUrl
from dotenv import load_dotenv
from typing import List, Annotated
import os
from datetime import datetime
from sqlalchemy.orm import Session
from auth_tools.get_user import get_current_user_modular

# Load environment variables
load_dotenv()

# Get the SECRET key from the environment
SECRET = os.getenv("SECRET_KEY")
DEBUG_SCRAPESCHOLAR = os.getenv("DEBUG_SCRAPESCHOLAR", "FALSE").upper() == "TRUE"

# Define OAuth2PasswordBearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter()


# Endpoint to retrieve the last 300 searches for the logged-in user
@router.get("/user/searches", status_code=status.HTTP_200_OK)
def get_last_300_searches(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    """
    Retrieve the last 300 searches for the logged-in user.
    """
    # verfies user is valid and has token
    current_user = get_current_user_modular(token=access_token, db=db)

    # Query the last 300 searches for the authenticated user
    searches = get_300_search(db=db, current_user=current_user)
    return searches if searches else []


# get single search and associated articles
@router.get("/user/articles", status_code=status.HTTP_200_OK)
def get_search_articles(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None,
                              search_id: int = Query(None, description="ID of the specific search to retrieve")):
    """
    Retrieve a single search and associated articles
    """
    #verifies user has a token and is valid
    get_current_user_modular(token=access_token, db=db)

    articles = get_full_article_response(db=db, search_id=search_id)
    return articles if articles else []

# get a searches title thinkt his duplicates above function except this one uses cookie...
# keeping it for now need to refactor these
@router.get("/user/search/title", status_code=status.HTTP_200_OK)
def get_search_title(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None,
                           search_id: int = Query(None, description="ID of the specific search to retrieve")):
    """
    Retrieve a single search and associtated articles
    """
    #verifies user has valid token
    current_user = get_current_user_modular(token=access_token, db=db)

    # Find the search
    search = find_search(db=db, current_user=current_user, search_id=search_id)
    return {'title': search.title, 'keywords': search.search_keywords} if search else []


# put a new title into a search
@router.put("/user/search/title", status_code=status.HTTP_200_OK)
def put_search_title(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None,
                           search_id: int = Query(None, description="ID of the specific search to retrieve"),
                           search_data: SearchUpdate = Body(...)):
    """
    Update the title of an existing search
    """
    #verifies user has valid token
    current_user = get_current_user_modular(token=access_token, db=db)

    # Query the last 300 searches for the authenticated user
    search = find_search(db=db, current_user=current_user, search_id=search_id)
    search.title = search_data.title
    db.commit()
    db.refresh(search)
    return search if search else []


# delete a search
@router.delete("/user/search/title", status_code=status.HTTP_200_OK)
def delete_search_title(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None,
                              search_id: int = Query(None, description="ID of the specific search to delete")):
    """
    delete a search and associated articles
    """
    #verifies user has valid token
    current_user = get_current_user_modular(token=access_token, db=db)

    search = find_search(db=db, current_user=current_user, search_id=search_id)

    if search is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Search not found")

    articles = find_search_articles(db, search_id)
    for article in articles:
        user_data = find_user_data(db, article.article_id)
        for data in user_data:
            db.delete(data)
        db.delete(article)
    db.delete(search)
    db.commit()
    return []


def find_search_articles(db, search_id):
    return (
        db.query(Article)
        .filter(Article.search_id == search_id)
        .order_by(Article.title.desc())
        .all()
    )


def find_user_data(db, article_id):
    return (
        db.query(UserData)
        .filter(UserData.article_id == article_id)
        .all()
    )


def find_search(db, current_user, search_id):
    try:
        search = (
            db.query(Search)
            .filter(Search.user_id == current_user.user_id, Search.search_id == search_id)
            .first()
        )
        return search
    except Exception as e:
        if DEBUG_SCRAPESCHOLAR:
            print(f"Error in find_search: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error finding search: {str(e)}")


def get_300_search(db, current_user):
    return (
        db.query(Search)
        .filter(Search.user_id == current_user.user_id)
        .order_by(Search.search_date.desc())
        .limit(300)
        .all()
    )


def check_if_user_exceeded_search_amount(db: Session, current_user: User):
    #check if there are 300 searches if there are return true
    existing_searches = get_300_search(db=db, current_user=current_user)
    if (len(existing_searches) >= 300):
        print("amount exceeded!")
        return True
    else:
        print("amount not exceeded")
        return False


def post_search_no_route(keywords: List[str], articles: List[ArticleBase], db: Session, current_user: User):
    """
    Save a search to the DB
    """

    """
    todo: 
    need to check if user has 300 searches, then respond with some kind of message to front 
    end to let it know to bug them to delete searches
    """

    result = check_if_user_exceeded_search_amount(db, current_user)

    if result:
        return False, None

    #title, date and user_id could this be better?
    decrypt_username = decrypt(current_user.username)
    title = f"{decrypt_username}-{datetime.now()}"
    # create new search to associate articles to
    search = SearchCreate(user_id=current_user.user_id, search_keywords=keywords, title=title)
    #add loop for 300 search here

    created_search = create_search(search=search, db=db)

    # Define the format
    date_format = "%Y-%m-%d"

    for article in articles:
        source = get_source_by_name(db, article.source)
        format_article= ArticleCreate(
        title=article.title,
        date=datetime.strptime(article.date, date_format).date(),
        link=HttpUrl(article.link),
        relevance_score=article.relevance_score,
        abstract=article.abstract,
        citedby=article.citedby,
        document_type=article.document_type,
        source_id=source.source_id,
        search_id=created_search.search_id, 
        user_id=current_user.user_id)
        create_article(article=format_article, db=db, user_id=current_user.user_id)
       
    

    return True, created_search.search_id


def get_full_article_response(db, search_id):
    articles = find_search_articles(db, search_id)
    response = []
    for article in articles:
        print("ARTICLE ID")
        print(article.article_id)

        user_data = get_user_data(db=db, article_id=article.article_id)

        source_name = get_source(db, article.source_id)
        article_data = SearchResult(
            article_id=article.article_id,
            title=article.title,
            date=article.date,
            citedby=article.citedby if article.citedby is not None else "?",
            link=article.link,
            abstract=article.abstract,
            document_type=article.document_type,
            source=source_name.name,
            methodology=user_data.methodology,
            clarity=user_data.clarity,
            transparency=user_data.transparency,
            completeness=user_data.completeness,
            evaluation_criteria=user_data.evaluation_criteria,
            color=user_data.relevancy_color,
            relevance_score=article.relevance_score
        )
        response.append(article_data)
    return response


def initialize_full_article_response(current_user: User, db, search_id):
    articles = find_search_articles(db, search_id)

    response = []
    for article in articles:
        user_data = create_user_data(db=db, user_id=current_user.user_id, article_id=article.article_id)

        source_name = get_source(db, article.source_id)

        article_data = SearchResult(
            article_id=article.article_id,
            title=article.title,
            date=article.date,
            citedby=article.citedby if article.citedby is not None else "?",
            link=article.link,
            abstract=article.abstract,
            document_type=article.document_type,
            source=source_name.name,
            methodology=user_data.methodology,
            clarity=user_data.clarity,
            transparency=user_data.transparency,
            completeness=user_data.completeness,
            color=user_data.relevancy_color,
            relevance_score=article.relevance_score
        )
        response.append(article_data)
    return response


