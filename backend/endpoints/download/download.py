# search/search.py
from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Query, Body
from fastapi.responses import StreamingResponse
from app.db.session import get_db
from typing import List, Annotated

from sqlalchemy.orm import Session
from auth_tools.get_user import get_current_user_modular
import endpoints.search.search as search
import csv
from io import StringIO
from typing import List, Dict, Generator

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def get_download(db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None,
                 search_id: int = Query(None, description="ID of the specific search to retrieve")):
    """
    Download a single search
    """
    #verifies user has a token and is valid
    get_current_user_modular(token=access_token, db=db)

    articles = search.get_full_article_response(db=db, search_id=search_id)
    article_title = search.get_search_title(db=db, search_id=search_id, access_token=access_token)
    article_title = article_title["title"]
    if not articles:
        return []
    else:
        return StreamingResponse(
            csv_generator(articles),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={article_title}.csv"}
        )


#should we add comments?

def csv_generator(data: List[Dict]) -> Generator[str, None, None]:
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=data[0].__dict__.keys())
    writer.writeheader()
    for row in data:
        writer.writerow(vars(row))
        buffer.seek(0)
        yield buffer.read()
        buffer.truncate(0)
        buffer.seek(0)
