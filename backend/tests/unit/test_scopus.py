from fastapi import FastAPI

from fastapi.testclient import TestClient

from app.main import app
from api_tools.api_tools import scopus_api_key

client = TestClient(app)




def test_scopus_apiKey_is_filled():
    assert scopus_api_key is not None
