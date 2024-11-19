# endpoints/user_data/user_data.py
from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from app.schemas.user_data import UserDataRead, UserDataUpdate
from app.crud.user_data import update_user_data
from app.db.session import get_db
from auth_tools.get_user import get_current_user_modular

router = APIRouter()


@router.put("/update", response_model=UserDataRead)
async def update_existing_user_data(
        user_data: UserDataUpdate,
        db: Session = Depends(get_db),
        access_token: str = Cookie(None)
):
    user = get_current_user_modular(token=access_token, db=db)
    user_role = user.role.role_name  # Extract the role name
    if user_data.evaluation_criteria is not None and user_role != "Professor":
        raise HTTPException(status_code=403, detail="Only professors can edit evaluation criteria")
    updated_user_data = await update_user_data(db=db, user_data=user_data, user_role=user_role,
                                               access_token=access_token)
    return updated_user_data
