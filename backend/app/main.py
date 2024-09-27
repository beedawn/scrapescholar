# app/main.py
from fastapi import FastAPI, Query
import academic_databases.sciencedirect.sciencedirect as sciencedirect
import academic_databases.scopus.scopus as scopus
from api_tools.api_tools import scopus_api_key
from fastapi.middleware.cors import CORSMiddleware
from role import role
from user import user
from auth import auth
from typing import List, Annotated

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

def check_response(response:List, id:int):
    if len(response) > 0 and response[-1].id is not None:
        new_id=response[-1].id+1
    else:
        new_id=id
    return new_id

@app.get("/academic_data")
async def multiple_apis(keywords:str, academic_databases: Annotated[List[str] | None, Query(alias="academic_database")] = None):
    print(academic_databases)
    response = []
    id = 0
    if "Science Direct" in academic_databases:
        new_id=check_response(response,id)
        article_response, id =sciencedirect.request_data(keywords, id=new_id)
        response.extend(article_response)
        print(response[-1])
    if "Scopus" in academic_databases:
        new_id=check_response(response,id)
        article_response, id =scopus.request_data(keywords, id=new_id)
        response.extend(article_response)
    return response


