
import pytest
from sqlalchemy.orm import Session
from app.crud.role import (
    get_role,
    get_roles,
    create_role,
    update_role,
    delete_role
)
from app.schemas.role import RoleCreate, RoleUpdate
from app.db.session import SessionLocal
from fastapi.exceptions import HTTPException
from datetime import datetime

def generate_unique_role_name(base_name="Role"):
    return f"{base_name}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

@pytest.fixture
def test_db_session():
    """Fixture to provide a database session with rollback for testing."""
    db = SessionLocal()
    db.begin_nested()

    yield db

    db.rollback()
    db.close()

def test_create_role(test_db_session: Session):
    """Test creating a new role."""
    role_name = generate_unique_role_name("PHD_Student")
    role_in = RoleCreate(role_name=role_name)
    created_role = create_role(test_db_session, role_in)

    assert created_role.role_name == role_name

def test_get_role(test_db_session: Session):
    """Test retrieving a role by ID."""
    role_name = generate_unique_role_name("PHD_Student")
    role_in = RoleCreate(role_name=role_name)
    created_role = create_role(test_db_session, role_in)

    fetched_role = get_role(test_db_session, created_role.role_id)
    assert fetched_role.role_id == created_role.role_id

def test_get_roles(test_db_session: Session):
    """Test retrieving a list of roles with pagination."""
    role_names = [generate_unique_role_name(name) for name in ["User", "Adjunct_Professor", "Project_Manager"]]
    role_data_list = [RoleCreate(role_name=name) for name in role_names]

    for role_data in role_data_list:
        create_role(test_db_session, role_data)

    roles = get_roles(test_db_session, skip=0, limit=2)
    assert len(roles) == 2

def test_update_role(test_db_session: Session):
    """Test updating a role."""
    role_name = generate_unique_role_name("PHD_Student")
    role_in = RoleCreate(role_name=role_name)
    created_role = create_role(test_db_session, role_in)

    updated_name = generate_unique_role_name("Updated_Role")
    update_data = RoleUpdate(role_name=updated_name)
    updated_role = update_role(test_db_session, created_role.role_id, update_data)

    assert updated_role.role_name == updated_name

def test_delete_role(test_db_session: Session):
    """Test deleting a role."""
    role_name = generate_unique_role_name("PHD_Student")
    role_in = RoleCreate(role_name=role_name)
    created_role = create_role(test_db_session, role_in)

    deleted_role = delete_role(test_db_session, created_role.role_id)
    assert deleted_role.role_id == created_role.role_id

    with pytest.raises(HTTPException) as exc_info:
        get_role(test_db_session, created_role.role_id)
    assert exc_info.value.status_code == 404

def test_get_role_not_found(test_db_session: Session):
    """Test error handling when a role is not found."""
    with pytest.raises(HTTPException) as exc_info:
        get_role(test_db_session, role_id=9999)
    assert exc_info.value.status_code == 404

def test_delete_role_not_found(test_db_session: Session):
    """Test error handling when trying to delete a non-existent role."""
    with pytest.raises(HTTPException) as exc_info:
        delete_role(test_db_session, role_id=9999)
    assert exc_info.value.status_code == 404