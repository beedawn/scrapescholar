# tests/integration/test_role_based_access_control.py

import pytest
import time
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db, SessionLocal
from app.models.role import Role
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url
from endpoints.auth.auth import login_manager 

client = TestClient(app)
session = get_cookie()

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def unique_username(base="user"):
    """Helper function to generate a unique username."""
    return f"{base}_{int(time.time())}"

@pytest.fixture
def ensure_roles_exist():
    """Fixture to ensure required roles exist in the database."""
    roles = ["Professor", "GradStudent", "Student"]
    db = SessionLocal()
    try:
        for role_name in roles:
            role = db.query(Role).filter_by(role_name=role_name).first()
            if not role:
                db.add(Role(role_name=role_name))
        db.commit()
    finally:
        db.close()

@pytest.fixture
def cleanup_users():
    """Fixture to create users and delete them after the test."""
    user_ids = []

    def _create_user(user_data):
        response = session.post(f"{base_url}/users/create", json=user_data)
        assert response.status_code == 201
        user_id = response.json()["user_id"]
        user_ids.append(user_id)
        return user_id

    yield _create_user

    # Cleanup: delete users after the test
    for user_id in user_ids:
        session.delete(f"{base_url}/users/delete/{user_id}")

def get_role_id_by_name(role_name):
    """Helper function to get the role ID based on the role name."""
    db = SessionLocal()
    try:
        role = db.query(Role).filter_by(role_name=role_name).first()
        return role.role_id if role else None
    finally:
        db.close()

def test_role_based_access_control(ensure_roles_exist, cleanup_users):
    create_user = cleanup_users

    # Create unique users with different roles
    prof_user_data = {
        "username": unique_username("professoruser"),
        "email": f"{unique_username('professoruser')}@example.com",
        "password": "password123",
    }
    grad_user_data = {
        "username": unique_username("gradstudent"),
        "email": f"{unique_username('gradstudent')}@example.com",
        "password": "password123",
    }
    student_user_data = {
        "username": unique_username("studentuser"),
        "email": f"{unique_username('studentuser')}@example.com",
        "password": "password123",
    }
    target_user_data = {
        "username": unique_username("targetuser"),
        "email": f"{unique_username('targetuser')}@example.com",
        "password": "password123",
    }

    prof_user_id = create_user(prof_user_data)
    grad_user_id = create_user(grad_user_data)
    student_user_id = create_user(student_user_data)
    target_user_id = create_user(target_user_data)

    # Assign roles to the created users
    session.put(f"{base_url}/users/update-role/{prof_user_id}", json={"role_name": "Professor"})
    session.put(f"{base_url}/users/update-role/{grad_user_id}", json={"role_name": "GradStudent"})
    session.put(f"{base_url}/users/update-role/{student_user_id}", json={"role_name": "Student"})

    # Generate tokens to simulate individual user access
    prof_token = login_manager.create_access_token(data={"sub": str(prof_user_id)})
    grad_token = login_manager.create_access_token(data={"sub": str(grad_user_id)})
    student_token = login_manager.create_access_token(data={"sub": str(student_user_id)})

    # Fetch the role IDs to validate
    grad_student_role_id = get_role_id_by_name("GradStudent")

    # Role assignment verification
    response = session.get(f"{base_url}/users/get/{target_user_id}")
    assert response.status_code == 200
    initial_role_name = "Student"

    # Step 1: Professor assigns "GradStudent" role to target user (should succeed)
    response = session.put(
        f"{base_url}/users/update-role/{target_user_id}",
        json={"role_name": "GradStudent"},
        cookies={"access_token": prof_token}  # Use Professor's token
    )
    assert response.status_code == 200
    assert response.json()["role_id"] == grad_student_role_id  # Validate against GradStudent role ID

    # Step 2: Graduate Student attempts to update the role of target user (should fail)
    response = session.put(
        f"{base_url}/users/update-role/{target_user_id}",
        json={"role_name": "Professor"},
        cookies={"access_token": grad_token}  # Use Graduate Student's token
    )
    assert response.status_code == 403  # Forbidden

    # Step 3: Student attempts to update the role of target user (should fail)
    response = session.put(
        f"{base_url}/users/update-role/{target_user_id}",
        json={"role_name": "Professor"},
        cookies={"access_token": student_token}  # Use Student's token
    )
    assert response.status_code == 403  # Forbidden

    # Step 4: Professor changes target user back to initial role (should succeed)
    response = session.put(
        f"{base_url}/users/update-role/{target_user_id}",
        json={"role_name": initial_role_name},
        cookies={"access_token": prof_token}
    )
    assert response.status_code == 200
    assert response.json()["role_id"] == get_role_id_by_name(initial_role_name)
