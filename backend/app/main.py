import requests
from fastapi import FastAPI
from fastapi.responses import FileResponse
import sciencedirect.sciencedirect as sciencedirect
import scopus.scopus as scopus
from api_tools.api_tools import sciencedirect_api_key
from api_tools.api_tools import scopus_api_key
from fastapi.middleware.cors import CORSMiddleware
from app.api import user, role, auth

app = FastAPI()

origins = [ "http://0.0.0.0:3000", "http://localhost:3000"]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        )

def status_check(get_response):
    if get_response == "200":
        return "Success 200:"
    
    elif get_response == "400":
        return "Error " + get_response + ": Invalid Request - Invalid information is submitted."
    
    elif get_response == "401":
        return "Error " + get_response + ": Authentication Error - User cannot be authenticated due to missing or invalid credentials (authtoken or APIKey)."
    
    elif get_response == "403":
        return "Error " + get_response + ": Authorization/Entitlements Error - User cannot be authenticated or entitlements cannot be validated."
    
    elif get_response == "405":
        return "Error " + get_response + ": Invalid HTTP Method - Requested HTTP Method is invalid."
    
    elif get_response == "406":
        return "Error " + get_response + ": Invalid Mime Type - Requested MIME type is invalid."
    
    elif get_response == "429":
        return "Error " + get_response + ": Quota Exceeded - Quota limits exceeded for associated API Key."
    
    elif get_response == "500":
        return "Error " + get_response + ": Generic Error - General-purpose error condition, typically due to back-end processing errors."

    else:
        return "Unknown Status Code: " + get_response

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
    getResponse = requests.get(response)
    if str(getResponse.status_code) == "200":
        csvFilePath = scopus.json_to_csv(getResponse.json())
        return FileResponse(path=csvFilePath, media_type='text/csv', filename="search_results_scopus.csv")
    else:
        return status_check(str(getResponse.status_code))

@app.get("/sciencedirect/json")
async def get_sciencedirect_data(keywords:str, apikey: str=sciencedirect_api_key, minYear:str="1990"):
    response = sciencedirect.query_science_direct_api(keywords, apikey, minYear)
    getResponse = requests.get(response)
    if str(getResponse.status_code) == "200":
        return getResponse.json()
    else:
        return status_check(str(getResponse.status_code))

@app.get("/sciencedirect/csv")
async def get_sciencedirect_data(keywords:str, apikey: str=sciencedirect_api_key, minYear:str="1990"):
    response = sciencedirect.query_science_direct_api(keywords, apikey, minYear)
    getResponse = requests.get(response)
    if str(getResponse.status_code) == "200":
        csvFilePath = sciencedirect.json_to_csv(getResponse.json())
        return FileResponse(path=csvFilePath, media_type='text/csv', filename="search_results_sciencedirect.csv")
    else:
        return status_check(str(getResponse.status_code))
    