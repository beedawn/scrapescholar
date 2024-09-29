# app/api/role.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.role import RoleCreate, RoleUpdate, RoleRead
from app.crud.role import get_role, get_roles, create_role, update_role, delete_role
from app.db.session import get_db

router = APIRouter()

@router.post("/create", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_new_role(role: RoleCreate, db: Session = Depends(get_db)):
    """
    API endpoint to create a new role.
    """
    new_role = create_role(db=db, role=role)
    return new_role

@router.get("/get/{role_id}", response_model=RoleRead)
def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to get a role by its ID.
    """
    role = get_role(db=db, role_id=role_id)
    return role

@router.get("/get-all", response_model=List[RoleRead])
def get_all_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    API endpoint to retrieve all roles.
    """
    roles = get_roles(db=db, skip=skip, limit=limit)
    return roles

@router.put("/update/{role_id}", response_model=RoleRead)
def update_existing_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    """
    API endpoint to update an existing role.
    """
    updated_role = update_role(db=db, role_id=role_id, role=role)
    return updated_role

@router.delete("/delete/{role_id}", response_model=RoleRead)
def delete_existing_role(role_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to delete a role by its ID.
    """
    deleted_role = delete_role(db=db, role_id=role_id)
    return deleted_role
