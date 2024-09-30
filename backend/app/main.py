# app/main.py
from fastapi import FastAPI, Query, Response, Request, Cookie
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
from endpoints.search.search import post_search

app = FastAPI()

origins = [ "http://0.0.0.0:3000", "http://localhost:3000"]

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

def check_response(response:List, id:int):
    if len(response) > 0 and response[-1].id is not None:
        new_id=response[-1].id+1
    else:
        new_id=id
    return new_id


def get_database_list(directory):
    # Get a list of all folders in the specified directory
    return [folder.name for folder in Path(directory).iterdir() if folder.is_dir() and folder.name != "__pycache__"]


@app.get("/academic_data")
async def multiple_apis(keywords:str, academic_databases: Annotated[List[str] | None, Query(alias="academic_database")] = None, 
cookie: Annotated[str | None, Cookie()] = None):
    print("cookies")
    print(cookie)

    response=[]
    id = 0
    database_list = get_database_list('academic_databases/')
    for item in database_list:
        if item in academic_databases:
            print(globals()[item])
            new_id=check_response(response,id)
            article_response, id =globals()[item].request_data(keywords, id=new_id)
            response.extend(article_response)
    # await post_search(keywords=keywords, articles=response)
    return response


@app.get("/academic_sources")
async def multiple_apis():
    database_list = get_database_list('academic_databases/')
    return database_list

@app.get("/cookie-time")
async def cookie_monster(response:Response):
    response.set_cookie(key="cookie", value="cookie")
    return {"message":"is cookie set?"}




@app.get("/cookie")
async def read_cookie(my_cookie: str | None = Cookie(None)):
    return {"cookie": my_cookie}