from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url

session = get_cookie()


def create_search():
    api_query = "test"
    query_string = "&academic_database=Scopus&academic_database=ScienceDirect"

    search_request = session.get(f"{base_url}/academic_data?keywords={api_query}{query_string}")
    search_request_data = search_request.json()
    search_id = search_request_data["search_id"]
    return search_id
