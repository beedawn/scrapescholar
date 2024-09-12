from fastapi import FastAPI
import sciencedirect.sciencedirect as sciencedirect
import scopus.scopus as scopus
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [ "http://0.0.0.0:3000"]


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
async def get_sciencedirect_data(query: str):
    return scopus.request_api(query)
