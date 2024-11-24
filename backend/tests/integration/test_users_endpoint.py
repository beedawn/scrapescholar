import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from endpoints.auth.auth import get_current_user
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from app.db.session import SessionLocal
import os
from tests.integration.tools.get_cookie import get_cookie
from tests.integration.tools.base_url import base_url
from tests.integration.tools.delete_user import delete_user


client = TestClient(app)
session = get_cookie()

load_dotenv()
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

fernet = Fernet(ENCRYPTION_KEY)

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="module")
def db_session():
    """Provides a transactional scope around a series of operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def decrypt_username(encrypted_username: str) -> str:
    """Helper function to decrypt the username manually during testing."""
    try:
        return fernet.decrypt(encrypted_username.encode()).decode()
    except Exception as e:
        print("Decryption failed:", e)
        raise


def override_get_current_user():
    return User(user_id=1, username="mockuser", email="mockuser@example.com", password="mockpassword")


@pytest.fixture
def client_with_mocked_auth():
    """Fixture to mock authentication by overriding the get_current_user dependency."""
    app.dependency_overrides[get_current_user] = override_get_current_user
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ----------------------- USER ENDPOINT TEST SUITE -----------------------
@pytest.mark.user
def test_create_user(db_session):
    """
    Test the user creation API endpoint.
    """
    user_data = {
        "username": "testuser2",
        "password": "testpassword",
        "email": "testuser@example.com"
    }

    response = session.post(f"{base_url}/users/create", json=user_data)

    assert response.status_code == 201

    created_user_id = response.json()["user_id"]

    db_session.commit()

    created_user = db_session.query(User).filter_by(user_id=created_user_id).first()

    assert created_user is not None
    decrypted_username = decrypt_username(created_user.username)
    assert decrypted_username == user_data["username"]
    assert hash_context.verify(user_data["password"], created_user.password)

    assert created_user.email != user_data["email"]
    assert created_user.email.startswith("$2b$")  # bcrypt hash prefix
    delete_user(created_user_id,session,base_url)

@pytest.mark.user
def test_get_user_by_id(db_session):
    """
    Test the API endpoint to retrieve a user by their user_id.
    """
    user_data = {
        "username": "testuser2",
        "password": "testpassword",
        "email": "testuser2@example.com"
    }
    response = session.post(f"{base_url}/users/create", json=user_data)
    assert response.status_code == 201
    created_user_id = response.json()["user_id"]

    db_session.commit()

    get_response = session.get(f"{base_url}/users/get/{created_user_id}")

    assert get_response.status_code == 200

    user = get_response.json()
    assert user["user_id"] == created_user_id
    assert user["email"].startswith("$2b$")  # Verify it's a bcrypt hash
    assert user["email"].startswith("$2b$")  # Ensure email is hashed
    delete_user(created_user_id, session, base_url)

