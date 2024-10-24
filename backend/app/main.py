# app/main.py
from fastapi import FastAPI, Query,Cookie, Depends
from fastapi.responses import JSONResponse

#needs these for globals call
import academic_databases.ScienceDirect.sciencedirect as ScienceDirect
import academic_databases.Scopus.scopus as Scopus
from api_tools.api_tools import scopus_api_key
#end of globals stuff
from app.db.session import get_db

from fastapi.middleware.cors import CORSMiddleware
from endpoints.role import role
from endpoints.user import user
from endpoints.auth import auth
from endpoints.user_data import user_data
from endpoints.search import search
from typing import List, Annotated
from pathlib import Path
from endpoints.search.search import post_search_no_route, check_if_user_exceeded_search_amount, \
    initialize_full_article_response
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from auth_tools.get_user import get_current_user_modular

app = FastAPI()

origins = ["http://0.0.0.0:3000", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health_check")
async def health_check():
    return {"message": "Hello World"}


# Include the auth routes in the main app
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(role.router, prefix="/roles", tags=["Roles"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(user_data.router, prefix="/user_data", tags=["UserData"])


def check_response(response: List, id: int):
    if len(response) > 0 and response[-1].article_id is not None:
        new_id = response[-1].article_id + 1
    else:
        new_id = id
    return new_id


async def get_database_list(directory):
    # Get a list of all folders in the specified directory
    return [folder.name for folder in Path(directory).iterdir() if folder.is_dir() and folder.name != "__pycache__"]


#to get the cookie the cookie value needs to be the same as the cookie key
#ie cookie key is access_token, so the parameter here needs to be access_token
@app.get("/academic_data")
async def multiple_apis(keywords: str,
                        academic_databases: Annotated[List[str] | None, Query(alias="academic_database")] = None,
                        access_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    current_user = await get_current_user_modular(token=access_token, db=db)
    exceeded_searches = await check_if_user_exceeded_search_amount(current_user=current_user, db=db)
    if exceeded_searches:
        return JSONResponse(
            status_code=507,
            content={"message": "Insufficient storage, you have 300 saved searches. Please delete some to continue"}
        )
    keywords_list = keywords.split()

    response = []
    id = 0
    database_list = await get_database_list('academic_databases/')
    for item in database_list:
        if item in academic_databases:
            new_id = check_response(response, id)
            article_response, id = globals()[item].request_data(keywords, id=new_id, )
            response.extend(article_response)
    #adds articles to db
    search_valid, search_id = await post_search_no_route(keywords=keywords_list, articles=response,
                                                         current_user=current_user, db=db)
    #instead of returning articles we're going to get the search from the db and return that
    articles = await initialize_full_article_response(current_user, db, search_id)

    if search_valid and search_id:
        return {"search_id": search_id, "articles": articles}
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "Not found."}
        )


@app.get("/academic_sources")
async def multiple_apis():
    database_list = await get_database_list('academic_databases/')
    return database_list
