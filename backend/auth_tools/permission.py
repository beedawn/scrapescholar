# backend/auth_tools/permission.py

from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.role import Role
from app.models.user import User
from auth_tools.get_user import get_current_user_modular # Adjust based on your auth setup

def is_professor(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_modular)):
    user_role = db.query(Role).filter(Role.role_id == current_user.role_id).first()
    if user_role.role_name != "Professor/Principal Investigator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
