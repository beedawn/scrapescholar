from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url

session = get_cookie()

#UT-1.2
# does not work consistently as this test is entirely dependent on Scopus and ScienceDirect results, which can change
# def test_user_data_slash_relevant_results():
#     test_word = "test"
#     searchdata = session.get(f"{base_url}/academic_data?keywords={test_word}&academic_database=Scopus&academic_database=ScienceDirect")

#     searchdata = searchdata.json()
#     found_word = False
#     for item in searchdata["articles"]:
#         for word in item["title"].split():
#             if test_word in word:
#                 found_word = True
#     assert found_word == True
#     search_id = searchdata["search_id"]
#     session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")



def test_user_data_slash_relevant_results_casing():
    searchdata = session.get(f"{base_url}/academic_data?keywords=test&academic_database=Scopus")
    searchdata_caps = session.get(f"{base_url}/academic_data?keywords=Test&academic_database=Scopus")
    searchdata = searchdata.json()
    searchdata_caps = searchdata_caps.json()
    searchdata_noid = []
    for item in searchdata["articles"]:
        searchdata_noid.append({
            "title": item["title"],
            "date": item["date"],
            "citedby": item["citedby"],
            "link": item["link"],
            "abstract": item["abstract"],
            "document_type": item["document_type"],
            "source": item["source"],
            "evaluation_criteria": item["evaluation_criteria"],
            "color": item["color"],
        }

        )
        searchdata_caps_noid = []
        for item in searchdata_caps["articles"]:
            searchdata_caps_noid.append({
                "title": item["title"],
                "date": item["date"],
                "citedby": item["citedby"],
                "link": item["link"],
                "abstract": item["abstract"],
                "document_type": item["document_type"],
                "source": item["source"],
                "evaluation_criteria": item["evaluation_criteria"],
                "color": item["color"],

            }

            )
    assert searchdata_noid == searchdata_caps_noid
    search_id = searchdata["search_id"]
    search_id_caps = searchdata_caps["search_id"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id_caps}")
