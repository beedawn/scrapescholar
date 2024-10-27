from fastapi import FastAPI

from fastapi.testclient import TestClient

from app.main import app
from app.main import check_response
from tests.integration.tools.get_cookie import get_cookie
from typing import List

client = TestClient(app)
session = get_cookie()
from tests.integration.tools.base_url import base_url

#UT-2.3
def test_academic_data_and():
    api_query = "test+AND+pizza"
    query_string = "&academic_database=Scopus&academic_database=ScienceDirect"
    search_request = session.get(f"{base_url}/academic_data?keywords={api_query}{query_string}")
    assert search_request.status_code ==200
    assert isinstance(search_request.json()["search_id"],int)
    assert isinstance(search_request.json()["articles"],List)