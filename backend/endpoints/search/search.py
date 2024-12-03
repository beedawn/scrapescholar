from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Query, Body
from app.db.session import get_db
from app.models.search import Search
from app.models.searchshare import SearchShare
from app.models.article import Article
from app.models.user import User
from app.models.user_data import UserData
from fastapi.security import OAuth2PasswordBearer
from app.crud.search import create_search, get_search
from app.crud.searchshare import create_search_share, get_search_share, get_search_share_by_search
from app.crud.source import get_source_by_name, get_source
from app.crud.user import decrypt, get_user_by_email, get_user_by_username
from app.schemas.search import SearchCreate, SearchUpdate
from app.schemas.article import ArticleCreate, ArticleBase
from app.schemas.searchshare import SearchShareCreate
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
from academic_databases.Scopus.scopus import sanitize_link_scopus
from academic_databases.ScienceDirect.sciencedirect import sanitize_link_sciencedirect
import validators

load_dotenv()

SECRET = os.getenv("SECRET_KEY")
DEBUG_SCRAPESCHOLAR = os.getenv("DEBUG_SCRAPESCHOLAR", "FALSE").upper() == "TRUE"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter()


@router.get("/user/searches", status_code=status.HTTP_200_OK)
def get_last_300_searches(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    """
    Retrieve the last 300 searches for the logged-in user.
    """
    current_user = get_current_user_modular(token=access_token, db=db)
    searches = get_300_search(db=db, current_user=current_user)
    shared_searches = get_shared_searches(db, current_user)
    searches = searches + shared_searches
    return searches if searches else []


@router.put("/share", status_code=status.HTTP_200_OK)
def put_search_share(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None,
                     search_id: int = Query(None, description="ID of the specific search to retrieve"),
                     share_user: str = Query(None, description="Username or Email of the specific user "
                                                               "to share search with")):
    user = get_current_user_modular(token=access_token, db=db)
    try:
        share_user_new = get_user_by_username(db, share_user)
        if share_user_new is None:
            share_user_new = get_user_by_email(db, share_user)
        if not share_user_new:
            raise HTTPException(status_code=404, detail="User not found by either username or email.")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    search_share = SearchShareCreate(search_id=search_id, shared_with_user_id=share_user_new.user_id,
                                     shared_by_user_id=user.user_id)
    created_share = create_search_share(db, search_share)
    return created_share


@router.get("/user/articles", status_code=status.HTTP_200_OK)
def get_search_articles(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None,
                        search_id: int = Query(None, description="ID of the specific search to retrieve")):
    """
    Retrieve a single search and associated articles
    """

    user = get_current_user_modular(token=access_token, db=db)
    search = get_search(db, search_id)
    match_search = None
    articles = None

    if search is None or search.user_id != user.user_id:
        searchshares = get_search_share_by_search(db, search_id)
        if searchshares is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        for searchshare in searchshares:
            if (searchshare.shared_with_user_id == user.user_id):
                match_search = searchshare
                break
    if (search is not None and search.user_id == user.user_id) or match_search is not None:
        articles = get_full_article_response(db=db, search_id=search_id)

    return articles if articles else []


@router.get("/user/search/title", status_code=status.HTTP_200_OK)
def get_search_title(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None,
                     search_id: int = Query(None, description="ID of the specific search to retrieve")):
    """
    Retrieve a single search and associtated articles
    """
    current_user = get_current_user_modular(token=access_token, db=db)
    search = find_search(db=db, current_user=current_user, search_id=search_id)
    return {'title': search.title, 'keywords': search.search_keywords} if search else []


@router.put("/user/search/title", status_code=status.HTTP_200_OK)
def put_search_title(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None,
                     search_id: int = Query(None, description="ID of the specific search to retrieve"),
                     search_data: SearchUpdate = Body(...)):
    """
    Update the title of an existing search
    """
    current_user = get_current_user_modular(token=access_token, db=db)
    search = find_search(db=db, current_user=current_user, search_id=search_id)
    search.title = search_data.title
    db.commit()
    db.refresh(search)
    return search if search else []


@router.delete("/user/search/title", status_code=status.HTTP_200_OK)
def delete_search_title(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None,
                        search_id: int = Query(None, description="ID of the specific search to delete")):
    """
    delete a search and associated articles
    """
    current_user = get_current_user_modular(token=access_token, db=db)

    search = find_search(db=db, current_user=current_user, search_id=search_id)
    if search is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Search not found")
    search_shares = get_search_share_by_search(db, search_id)
    if search_shares is not None:
        for share in search_shares:
            if share.shared_by_user_id == current_user.user_id:
                db.delete(share)
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
        if search is None:
            search = (
                db.query(Search)
                .join(SearchShare, Search.search_id == SearchShare.search_id)
                .filter(SearchShare.shared_with_user_id == current_user.user_id)
                .filter(Search.search_id == search_id)
                .order_by(Search.search_date.desc())
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


def get_shared_searches(db, current_user):
    shared_searches = (
        db.query(Search)
        .join(SearchShare, Search.search_id == SearchShare.search_id)
        .filter(SearchShare.shared_with_user_id == current_user.user_id)
        .order_by(Search.search_date.desc())
        .all()
    )
    return shared_searches


def check_if_user_exceeded_search_amount(db: Session, current_user: User):
    existing_searches = get_300_search(db=db, current_user=current_user)
    if len(existing_searches) >= 300:
        print("amount exceeded!")
        return True
    else:
        print("amount not exceeded")
        return False


def post_search_no_route(keywords: List[str], articles: List[ArticleBase], db: Session, current_user: User):
    """
    Save a search to the DB
    """
    result = check_if_user_exceeded_search_amount(db, current_user)

    if result:
        return False, None

    decrypt_username = decrypt(current_user.username)
    title = f"{decrypt_username}-{datetime.now()}"
    search = SearchCreate(user_id=current_user.user_id, search_keywords=keywords, title=title)
    created_search = create_search(search=search, db=db)
    date_format = "%Y-%m-%d"
    for article in articles:
        source = get_source_by_name(db, article.source)
        format_article = ArticleCreate(
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
        if source_name == "Scopus":
            parsed_link = sanitize_link_scopus(article.link)
        elif source_name == "ScienceDirect":
            parsed_link = sanitize_link_sciencedirect(article.link)


        else:
            if validators.url(article.link):
                parsed_link = article.link
            else:
                parsed_link = "Potentially malicious link detected. Blocked for user safety."
        article_data = SearchResult(
            article_id=article.article_id,
            title=article.title,
            date=article.date,
            citedby=article.citedby if article.citedby is not None else "?",
            link=parsed_link,
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
