from fastapi import FastAPI

from fastapi.testclient import TestClient
from tests.integration.tools.get_cookie import get_cookie
from app.main import app
from tests.integration.tools.base_url import base_url
client = TestClient(app)
session = get_cookie()

def test_read_main():
    response = client.get("/health_check")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
