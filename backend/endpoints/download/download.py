# search/search.py
from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Query, Body
from fastapi.responses import StreamingResponse
from app.db.session import get_db
from typing import List, Annotated

from sqlalchemy.orm import Session
from auth_tools.get_user import get_current_user_modular
import endpoints.search.search as search
from endpoints.comment.comment import get_comments_no_token
import csv
from io import StringIO
from typing import List, Dict, Generator
from app.crud.user import get_user, decrypt

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
    search_title = search.get_search_title(db=db, search_id=search_id, access_token=access_token)
    search_title = search_title["title"]
    if not articles:
        return []
    else:
        return StreamingResponse(
            csv_generator(articles, db),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={search_title}.csv"}
        )


def csv_generator(data: List, db) -> Generator[str, None, None]:
    buffer = StringIO()
    fieldnames = build_fieldnames(data)
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        row_data = add_user_comments_to_list(row,db)
        writer.writerow(row_data)
        buffer.seek(0)
        yield buffer.read()
        buffer.truncate(0)
        buffer.seek(0)


def build_fieldnames(data):
    comment_headers = []
    user_name_headers = []
    i = 1
    while i <= 100:
        comment_headers.append(f"Comment {i}")
        user_name_headers.append(f"Username Comment {i}")
        i += 1
    fieldnames = list(data[0].__dict__.keys())
    for comment, user in zip(comment_headers, user_name_headers):
        fieldnames.append(user)
        fieldnames.append(comment)
    return fieldnames


def add_user_comments_to_list(row, db):
    article_comment = get_comments_no_token(db=db, article_id=row.article_id)
    row_data = vars(row)
    for i, comment_builder in enumerate(article_comment, start=1):
        user = get_user(db, comment_builder["user_id"])
        row_data[f"Username Comment {i}"] = decrypt(user.username)
        row_data[f"Comment {i}"] = comment_builder["comment_text"]
    return row_data
