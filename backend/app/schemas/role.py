# app/schemas/role.py
from pydantic import BaseModel

class RoleBase(BaseModel):
    role_name: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    role_name: Optional[str] = None

class RoleRead(RoleBase):
    role_id: int

    class Config:
        orm_mode = True