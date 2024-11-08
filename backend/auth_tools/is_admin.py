from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from auth_tools.get_user import get_current_user_modular

from sqlalchemy.orm import Session
from app.db.session import get_db

def is_admin(access_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    user = get_current_user_modular(access_token, db)

    if user.role_id == 1:
        return True
    else:
        return False
