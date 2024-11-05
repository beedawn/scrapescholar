import pytest
from endpoints.download.download import csv_generator, build_fieldnames, add_user_comments_to_list
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url
from academic_databases.SearchResult import SearchResult
from io import StringIO
from tests.integration.tools.create_search import create_search
import csv

session = get_cookie()


@pytest.fixture
def test_db_session():
    """Fixture to provide a database session for testing"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#UT-8.2
def test_generate_data(test_db_session: Session):
    api_query = "test"
    query_string = "&academic_database=Scopus&academic_database=ScienceDirect"
    search_request = session.get(f"{base_url}/academic_data?keywords={api_query}{query_string}")
    search_request = search_request.json()
    search_id = search_request["search_id"]
    articles = search_request["articles"]
    search_articles = []
    for item in articles:
        search_articles.append(SearchResult(**item))
    #join generator into string
    csv_result = ""
    for chunk in csv_generator(search_articles, test_db_session):
        csv_result += chunk
    #build field names
    fieldnames = build_fieldnames(search_articles)
    #generate csv
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    #write csv
    for row in search_articles:
        #inject comments and usernames
        row_data = add_user_comments_to_list(row, test_db_session)
        writer.writerow(row_data)

    test_result = buffer.getvalue()
    buffer.close()

    assert csv_result == test_result
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")



# UT-8.3
def test_csv_filename_in_response():
    search_id = create_search()
    response = session.get(f"{base_url}/download?search_id={search_id}")
    content_disposition = response.headers["Content-Disposition"]
    #get title
    response = session.get(f"{base_url}/search/user/search/title?search_id={search_id}")
    response = response.json()
    title = response["title"]
    #compare search title to downloaded filed
    assert f'attachment; filename={title}' in content_disposition
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")


