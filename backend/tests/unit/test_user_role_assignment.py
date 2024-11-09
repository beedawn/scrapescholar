import pytest
import time
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db, SessionLocal
from app.models.role import Role
from sqlalchemy.exc import OperationalError
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url

client = TestClient(app)
session = get_cookie()

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def unique_username(base="testuser"):
    return f"{base}_{int(time.time())}"

@pytest.fixture(scope="module")
def setup_roles():
    """Ensure required roles exist in the database."""
    db = SessionLocal()
    roles = ["Professor", "GradStudent"]
    for role_name in roles:
        if not db.query(Role).filter_by(role_name=role_name).first():
            db.add(Role(role_name=role_name))
    db.commit()
    db.close()

@pytest.fixture
def cleanup_user():
    user_ids = []

    def _create_user(user_data):
        response = session.post(f"{base_url}/users/create", json=user_data)
        assert response.status_code == 201
        user_id = response.json()["user_id"]
        user_ids.append(user_id)
        return user_id

    yield _create_user

    for user_id in user_ids:
        session.delete(f"{base_url}/users/delete/{user_id}")

def get_role_id(role_name, retries=3, delay=2):
    db = SessionLocal()
    role_id = None
    for attempt in range(retries):
        try:
            role = db.query(Role).filter(Role.role_name == role_name).first()
            role_id = role.role_id if role else None
            break
        except OperationalError:
            time.sleep(delay)
        finally:
            db.close()
    return role_id

def test_assign_role_to_user(cleanup_user, setup_roles):
    user_data = {
        "username": unique_username(),
        "email": f"{unique_username()}@example.com",
        "password": "password123",
    }
    user_id = cleanup_user(user_data)

    response = session.put(f"{base_url}/users/update-role/{user_id}", json={"role_name": "Professor"})
    assert response.status_code == 200
    assert response.json()["role_id"] == get_role_id("Professor")

    response = session.put(f"{base_url}/users/update-role/{user_id}", json={"role_name": "GradStudent"})
    assert response.status_code == 200
    assert response.json()["role_id"] == get_role_id("GradStudent")
