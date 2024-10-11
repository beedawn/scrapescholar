# endpoints/user_data/user_data.py
from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.schemas.user_data import UserDataBase, UserDataCreate, UserDataRead, UserDataUpdate
from app.crud.user_data import create_user_data, update_user_data
from app.db.session import get_db
from endpoints.search.search import get_current_user_no_route

router = APIRouter()

# @router.post("/create", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
# def create_new_role(role: RoleCreate, db: Session = Depends(get_db)):
#     """
#     API endpoint to create a new role.
#     """
#     new_role = create_role(db=db, role=role)
#     return new_role

# @router.get("/get/{role_id}", response_model=RoleRead)
# def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
#     """
#     API endpoint to get a role by its ID.
#     """
#     role = get_role(db=db, role_id=role_id)
#     return role

# @router.get("/get-all", response_model=List[RoleRead])
# def get_all_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     """
#     API endpoint to retrieve all roles.
#     """
#     roles = get_roles(db=db, skip=skip, limit=limit)
#     return roles

@router.put("/update", response_model=UserDataRead)
async def update_existing_user_data(user_data: UserDataUpdate, db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    """
    API endpoint to update an existing user_data.
    """
    print("Access token")
    print(access_token)
    user = await get_current_user_no_route(db=db, token=access_token)
    if user is not None:
        updated_user_data = await update_user_data(db=db, user_data=user_data)
        return updated_user_data
    else:
        return []

# @router.delete("/delete/{role_id}", response_model=RoleRead)
# def delete_existing_role(role_id: int, db: Session = Depends(get_db)):
#     """
#     API endpoint to delete a role by its ID.
#     """
#     deleted_role = delete_role(db=db, role_id=role_id)
#     return deleted_role
