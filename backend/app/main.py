# app/main.py
from fastapi import FastAPI, Query, Response, Request, Cookie, Depends
import academic_databases.ScienceDirect.sciencedirect as ScienceDirect
import academic_databases.Scopus.scopus as Scopus
from api_tools.api_tools import scopus_api_key
from fastapi.middleware.cors import CORSMiddleware
from endpoints.role import role
from endpoints.user import user
from endpoints.auth import auth
from endpoints.search import search
from typing import List, Annotated
from pathlib import Path
from endpoints.search.search import post_search_no_route, get_current_user_no_route
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
    print(keywords)
    keywords_list = keywords.split()
    response=[]
    id = 0
    database_list = get_database_list('academic_databases/')
    for item in database_list:
        if item in academic_databases:
            print(globals()[item])
            new_id=check_response(response,id)
            article_response, id =globals()[item].request_data(keywords, id=new_id,)
            response.extend(article_response)
            for x in article_response:
                print(x.__dict__)
            print(article_response)
    current_user= await get_current_user_no_route(token=access_token, db=db)
    await post_search_no_route(keywords=keywords_list, articles=response, current_user=current_user, db=db)
    return response


@app.get("/academic_sources")
async def multiple_apis():
    database_list = get_database_list('academic_databases/')
    return database_list

@app.post("/set_cookie")
async def set_cookie(response: Response):
    response.set_cookie(key="my_cookie", value="cookie_value")
    return {"message": "Cookie set"}


@app.get("/cookie")
async def read_cookie(my_cookie: str | None = Cookie(None)):
    return {"cookie": my_cookie}