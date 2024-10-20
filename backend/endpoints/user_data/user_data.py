# endpoints/user_data/user_data.py
from fastapi import APIRouter, Depends, Cookie
from sqlalchemy.orm import Session
from typing import Annotated
from app.schemas.user_data import UserDataRead, UserDataUpdate
from app.crud.user_data import update_user_data
from app.db.session import get_db
from auth_tools.get_user import get_current_user_modular

router = APIRouter()


@router.put("/update", response_model=UserDataRead)
async def update_existing_user_data(user_data: UserDataUpdate, db: Session = Depends(get_db),
                                    access_token: Annotated[str | None, Cookie()] = None):
    """
    API endpoint to update an existing user_data.
    """
    #checks user has valid token
    user = await get_current_user_modular(db=db, token=access_token)
    if user is not None:
        updated_user_data = await update_user_data(db=db, user_data=user_data)
        return updated_user_data
    else:
        return []


