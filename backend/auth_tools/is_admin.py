from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from auth_tools.get_user import get_current_user_modular
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.role import Role

def is_admin(access_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    user = get_current_user_modular(access_token, db)

    # Retrieve the user's role by role_id and check the role name
    role = db.query(Role).filter(Role.role_id == user.role_id).first()
    
    if role and role.role_name == "Professor":
        return True
    else:
        return False
