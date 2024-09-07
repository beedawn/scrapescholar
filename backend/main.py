from fastapi import FastAPI

app = FastAPI()


@app.get("/health_check")
async def root():
    return {"message": "Hello World"}
