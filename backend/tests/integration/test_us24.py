from fastapi.testclient import TestClient
from app.main import app
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url
from api_tools.api_tools import scopus_inst_token
from tests.integration.tools.blankAPIKey import request_body
session = get_cookie()
client = TestClient(app)


def test_abstract_is_in_response():
    if scopus_inst_token is not None:
        searchdata = session.post(f"{base_url}/academic_data?keywords=test&academic_database=Scopus", json=request_body)
        searchdata = searchdata.json()
        for item in searchdata["articles"]:
            assert item["abstract"] is not None

        search_id = searchdata["search_id"]

        session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")

    else:
        assert True
