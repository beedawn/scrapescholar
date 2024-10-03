from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from api_tools.api_tools import sciencedirect_api_key

client = TestClient(app)
#todo
#get access token from login endpoint
#mimic cookie so that these tests will pass



   


def test_sciencedirect_apiKey_env_is_filled():
    assert sciencedirect_api_key is not None
