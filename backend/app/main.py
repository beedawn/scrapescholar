# app/main.py
from fastapi import FastAPI
import sciencedirect.sciencedirect as sciencedirect
import scopus.scopus as scopus
from api_tools.api_tools import scopus_api_key
from fastapi.middleware.cors import CORSMiddleware
from role import role
from user import user
from auth import auth

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

@app.get("/sciencedirect")
async def get_sciencedirect_data(query: str):
    return sciencedirect.request_api(query)


@app.get("/scopus")
async def researcher_api_call(keywords:str, apikey: str=scopus_api_key, subject:str="", minYear:str="1990"):
    response = scopus.query_scopus_api(keywords, apikey, subject, minYear)
    return response

    # Use later for json to csv frontend
    csvFilePath = scopus.load_json_scrape_results(jsonResults)
    return FileResponse(path=csvFilePath, media_type='text/csv', filename="search_results.csv")