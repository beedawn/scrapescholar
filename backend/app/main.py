# app/main.py
from fastapi import FastAPI, Query, Response, Request, Cookie, Depends
from fastapi.responses import JSONResponse
import academic_databases.ScienceDirect.sciencedirect as ScienceDirect
import academic_databases.Scopus.scopus as Scopus
from api_tools.api_tools import scopus_api_key
from fastapi.middleware.cors import CORSMiddleware
from endpoints.role import role
from endpoints.user import user
from endpoints.auth import auth
from endpoints.search import search
from endpoints.article import article
from endpoints.comment import comment
from typing import List, Annotated
from pathlib import Path
from endpoints.search.search import post_search_no_route, get_current_user_no_route, check_if_user_exceeded_search_amount
from app.db.session import get_db, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

origins = [ "http://0.0.0.0:3000", "http://localhost:3000"]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health_check")
async def health_check():
    return {"message": "Hello World"}

# Include the auth routes in the main app
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(role.router, prefix="/roles", tags=["Roles"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(article.router, prefix="/articles", tags=["Articles"])
app.include_router(comment.router, prefix="/comments", tags=["Comments"])

def check_response(response:List, id:int):
    if len(response) > 0 and response[-1].id is not None:
        new_id=response[-1].id+1
    else:
        new_id=id
    return new_id


def get_database_list(directory):
    # Get a list of all folders in the specified directory
    return [folder.name for folder in Path(directory).iterdir() if folder.is_dir() and folder.name != "__pycache__"]

#to get the cookie the cookie value needs to be the same as the cookie key

#ie cookie key is access_token, so the parameter here needs to be access_token
@app.get("/academic_data")
async def multiple_apis(keywords:str, academic_databases: Annotated[List[str] | None, Query(alias="academic_database")] = None, 
access_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    current_user= await get_current_user_no_route(token=access_token, db=db)
    exceeded_searches = await check_if_user_exceeded_search_amount(current_user=current_user, db=db)
    if exceeded_searches:
        return JSONResponse(
        status_code=507,
        content={"message": "Insufficient storage, you have 300 saved searches. Please delete some to continue"}
        )
    keywords_list = keywords.split()
    print("USER ID")
    print(current_user.user_id)
    response=[]
    id = 0
    database_list = get_database_list('academic_databases/')
    for item in database_list:
        if item in academic_databases:
            new_id=check_response(response,id)
            article_response, id =globals()[item].request_data(keywords, id=new_id,)
            response.extend(article_response)
    #need something here to get search id after its made or associated function
    search_valid, search_id = await post_search_no_route(keywords=keywords_list, articles=response, current_user=current_user, db=db)
    if search_valid and search_id:
        return {"search_id":search_id, "articles":response}
    else:
        return JSONResponse(
        status_code=404,
        content={"message": "Not found."}
    )


@app.get("/academic_sources")
async def multiple_apis():
    database_list = get_database_list('academic_databases/')
    return database_list

