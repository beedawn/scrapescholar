from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
import time
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url

session = get_cookie()
#UT-23.1
client = TestClient(app)
def test_user_data_slash_update_put_valid_body():
    searchdata=session.get(f"{base_url}/academic_data?keywords=test&academic_database=Scopus")
    data = {
  "article_id":1,
  "relevancy_color": "Not Relevant",
  "evaluation_criteria":"Pending",
  "methodology":"0",
  "clarity": "0",
  "transparency": "1",
  "completeness": "1"
}
    putrequest=session.put(f"{base_url}/user_data/update", json=data)
    response = session.get(f"{base_url}/search/user/articles?search_id=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        if item["article_id"]==1:
            assert item["color"] == "Not Relevant" 
            assert item["evaluation_criteria"] == "Pending"
            assert item["methodology"] ==0
            assert item["clarity"]==0
            assert item["transparency"]==1
            assert item["completeness"]==1
    searchdata=searchdata.json()
    search_id=searchdata["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")

#UT-23.2
def test_user_data_slash_update_put_no_cookie():
    searchdata=session.get(f"{base_url}/academic_data?keywords=test&academic_database=Scopus")
    data = {
  "article_id":1,
  "relevancy_color": "Not Relevant",
  "evaluation_criteria":"Pending",
  "methodology":"0",
  "clarity": "0",
  "transparency": "1",
  "completeness": "1"
}
    putrequest=client.put(f"{base_url}/user_data/update", json=data)
    assert putrequest.status_code == 401
    # response = session.get(f"{base_url}/search/user/articles?search_id=1")
    # assert response.status_code == 200
    data = putrequest.json()
    
    assert data["detail"] == "Invalid token" 


#UT-23.3     
def test_user_data_slash_update_put_invalid_body():
    searchdata=session.get(f"{base_url}/academic_data?keywords=test&academic_database=Scopus")
    data = {
  "relevancy_color": "Not Relevant",
}
    putrequest=session.put(f"{base_url}/user_data/update", json=data)
    assert putrequest.status_code == 422
    # response = session.get(f"{base_url}/search/user/articles?search_id=1")
    # assert response.status_code == 200
    data = putrequest.json()
    
  
    assert isinstance(data["detail"], list)
    assert data["detail"][0]["type"] == "missing" 
    assert isinstance(data["detail"][0]["loc"], list)
    assert data["detail"][0]["loc"][0] == "body" 
    assert data["detail"][0]["loc"][1] == "article_id" 
    assert data["detail"][0]["msg"] == "Field required" 
    assert data["detail"][0]["input"]["relevancy_color"]=="Not Relevant"


     