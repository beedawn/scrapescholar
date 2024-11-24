from fastapi import APIRouter, Depends, status, Cookie, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.role import RoleCreate, RoleUpdate, RoleRead
from app.crud.role import get_role, get_roles, create_role, update_role, delete_role
from app.db.session import get_db
from auth_tools.get_user import get_current_user_modular
from auth_tools.is_admin import is_admin
from typing import Annotated

router = APIRouter()

@router.post("/create", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
async def create_new_role(
    role: RoleCreate,
    access_token: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db)
):
    """
    API endpoint to create a new role.
    """
    get_current_user_modular(token=access_token, db=db)
    if not is_admin(access_token, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    new_role = create_role(db=db, role=role)
    return new_role

@router.get("/get/{role_id}", response_model=RoleRead)
async def get_role_by_id(
    role_id: int,
    access_token: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db)
):
    """
    API endpoint to get a role by its ID.
    """
    get_current_user_modular(token=access_token, db=db)
    role = get_role(db=db, role_id=role_id)
    return role

@router.get("/get-all", response_model=List[RoleRead])
async def get_all_roles(
    access_token: Annotated[str | None, Cookie()] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    API endpoint to retrieve all roles.
    """
    get_current_user_modular(token=access_token, db=db)
    roles = get_roles(db=db, skip=skip, limit=limit)
    return roles

@router.put("/update/{role_id}", response_model=RoleRead)
async def update_existing_role(
    role_id: int,
    role: RoleUpdate,
    access_token: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db)
):
    """
    API endpoint to update an existing role.
    """
    get_current_user_modular(token=access_token, db=db)
    if not is_admin(access_token, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    updated_role = update_role(db=db, role_id=role_id, role=role)
    return updated_role


@router.delete("/delete/{role_id}", response_model=RoleRead)
async def delete_existing_role(
    role_id: int,
    access_token: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db)
):
    """
    API endpoint to delete a role by its ID.
    """
    get_current_user_modular(token=access_token, db=db)
    if not is_admin(access_token, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    deleted_role = delete_role(db=db, role_id=role_id)
    return deleted_role
