from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from api_tools.api_tools import sciencedirect_api_key
client = TestClient(app)
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url

session = get_cookie()
#UT-5.2
async def test_user_data_slash_update_put():
    data = {
    "article_id": 1,
    "relevancy_color": "Not Relevant"
    }
    await session.put(f"{base_url}/user_data/update", json=data)
    apiQuery="test"
    queryString="&academic_database=Scopus&academic_database=ScienceDirect"
    response = await session.get(f"{base_url}/academic_data?keywords={apiQuery}{queryString}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["articles"], list)
    for item in data["articles"]:
        print(item)
        if item["article_id"]==1:
            assert item["color"] == "Not Relevant" 

