from fastapi import FastAPI
import backend.sciencedirect

app = FastAPI()


@app.get("/health_check")
async def health_check():
    return {"message": "Hello World"}



@app.get("/sciencedirect")
async def get_sciencedirect_data():
    result=backend.sciencedirect.request_api()
    return result
