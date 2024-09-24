from fastapi import FastAPI
import sciencedirect.sciencedirect as sciencedirect
import scopus.scopus as scopus
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/sciencedirect")
async def get_sciencedirect_data(query: str):
    return sciencedirect.request_api(query)


@app.get("/scopus")
async def researcher_api_call(keywords, apikey: str=scopus.scopus_api_key, subject:str="", minYear:str="1990"):

    #searchQuery = scopus.QueryParameters(keywords=keywordsList, subject=subject, minYear=minYear)
    response = scopus.query_scopus_api(keywords, apikey, subject, minYear)
    
    return response

    # Use later for json to csv frontend
    csvFilePath = scopus.load_json_scrape_results(jsonResults)
    return FileResponse(path=csvFilePath, media_type='text/csv', filename="search_results.csv")
