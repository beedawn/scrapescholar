from fastapi.testclient import TestClient
from app.main import app
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url

client = TestClient(app)
session = get_cookie()


#UT-3.2
def test_academic_data_21_keywords():
    query_string = "a%20AND%20b%20AND%20c%20AND%20d%20AND%20e%20AND%20f%20AND%20e%20AND%20f%20AND%20g%20AND%20h%20AND%20i%20AND%20j%20AND%20k%20AND%20l%20AND%20m%20AND%20n%20AND%20o%20AND%20p%20AND%20q%20AND%20q%20AND%20q&academic_database=Scopus&academic_database=ScienceDirect"
    search_request = session.get(f"{base_url}/academic_data?keywords={query_string}")
    assert search_request.status_code == 413
    search_request_data = search_request.json()
    message = search_request_data["message"]

    assert isinstance(message, str)
    assert message == "Too many keywords"


#UT-3.3
def test_academic_data_20_keywords():
    query_string = "apple%20AND%20banana%20AND%20carrot%20AND%20donut%20AND%20egg%20AND%20flapjack%20AND%20egg%20AND%20fry%20AND%20grape%20AND%20hotdog%20AND%20igloo%20AND%20jam%20AND%20king%20AND%20lemon%20AND%20mango%20AND%20night%20AND%20orange%20AND%20pickle%20AND%20queen%20AND%20queen&academic_database=Scopus&academic_database=ScienceDirect"
    search_request = session.get(f"{base_url}/academic_data?keywords={query_string}")
    assert search_request.status_code == 200
    search_request_data = search_request.json()
    search_id = search_request_data["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
