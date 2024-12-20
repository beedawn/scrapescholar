from fastapi.testclient import TestClient
from api_tools.api_tools import scopus_inst_token
from app.main import app
from tests.integration.tools.get_cookie import get_cookie
from typing import List
from tests.integration.tools.base_url import base_url
from tests.integration.tools.blankAPIKey import request_body
client = TestClient(app)
session = get_cookie()

#UT-2.3
def test_academic_data_and():
    keyword_one="yogurt"
    keyword_two="milk"
    api_query = f"{keyword_one}%20AND%20{keyword_two}"
    query_string = "&academic_database=Scopus&academic_database=ScienceDirect"
    search_request = session.post(f"{base_url}/academic_data?keywords={api_query}{query_string}", json=request_body)
    assert search_request.status_code ==200
    search_request_data = search_request.json()
    search_id = search_request_data["search_id"]
    assert isinstance(search_request_data["search_id"],int)
    assert isinstance(search_request_data["articles"], List)
    keyword_one_found = False
    keyword_two_found = False
    for item in search_request_data["articles"]:
        if keyword_one in item["title"]:
            keyword_one_found = True
        if keyword_two in item["title"]:
            keyword_two_found = True
    assert keyword_one_found == True
    assert keyword_two_found == True
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


def test_academic_data_NOT():
    keyword_one="lemon"
    keyword_two="pizza"
    api_query = f"{keyword_one}%20AND%20NOT%20{keyword_two}"
    query_string = "&academic_database=Scopus"
    search_request = session.post(f"{base_url}/academic_data?keywords={api_query}{query_string}", json=request_body)
    assert search_request.status_code ==200
    search_request_data = search_request.json()
    search_id = search_request_data["search_id"]
    assert isinstance(search_request_data["search_id"],int)
    assert isinstance(search_request_data["articles"], List)
    keyword_one_found = False
    keyword_two_found = False
    for item in search_request_data["articles"]:
        if keyword_one in item["title"].lower():
            keyword_one_found = True
        if keyword_two in item["title"].lower():
            keyword_two_found = True
        if item["abstract"] and scopus_inst_token is not None:
            if keyword_one in item["abstract"].lower():
                keyword_one_found = True
            if keyword_two in item["abstract"].lower():
                keyword_two_found = True
    assert keyword_one_found == True
    assert keyword_two_found == False
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")