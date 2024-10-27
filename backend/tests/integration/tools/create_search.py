from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url

session = get_cookie()


def create_search():
    # Step 3: Create a search and pass user_id dynamically
    api_query = "test"
    query_string = "&academic_database=Scopus&academic_database=ScienceDirect"
    # create a new search to query

    search_request = session.get(f"{base_url}/academic_data?keywords={api_query}{query_string}")
    print(search_request)
    search_request_data = search_request.json()
    search_id = search_request_data["search_id"]
    return search_id
