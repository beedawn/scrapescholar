import pytest
from endpoints.download.download import csv_generator, build_fieldnames, add_user_comments_to_list
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url
from academic_databases.SearchResult import SearchResult

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
    search_request =search_request.json()
    search_id=search_request["search_id"]
    articles = search_request["articles"]
    search_articles = []
    for item in articles:
        search_articles.append(SearchResult(**item))
    chunks = list(csv_generator(search_articles, test_db_session))
    fieldnames = build_fieldnames(search_articles)
    final_result = fieldnames
    for item in search_articles:
        row = add_user_comments_to_list(item, test_db_session)
        print(row)
        final_result.append(row)

    print("-----------------CHUNKS---------")
    print(chunks)
    print("-----------------FINAL RESULT---------")
    print(final_result)
    # Verify the output matches expected chunks
    # assert chunks == ["chunk 0\n", "chunk 1\n", "chunk 2\n", "chunk 3\n", "chunk 4\n"]
    session.delete(f"{base_url}/search/user/search/title?search_id={search_id}")