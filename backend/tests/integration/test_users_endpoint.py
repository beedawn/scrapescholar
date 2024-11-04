# tests/unit/test_users_endpoint.py
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

# Initialize TestClient
client = TestClient(app)
session = get_cookie()
# Load environment variables
load_dotenv()
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
print("Loaded ENCRYPTION_KEY:", os.getenv("ENCRYPTION_KEY"))
# Create a Fernet object for encryption/decryption
fernet = Fernet(ENCRYPTION_KEY)

# Password hashing context
hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="module")
def db_session():
    """Provides a transactional scope around a series of operations."""
    db = SessionLocal()  # Assuming SessionLocal is defined in your app to connect to the database
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
        raise  # Re-raise or handle as needed


# Mocking the get_current_user dependency to return a test user
def override_get_current_user():
    return User(user_id=1, username="mockuser", email="mockuser@example.com", password="mockpassword")


@pytest.fixture
def client_with_mocked_auth():
    """Fixture to mock authentication by overriding the get_current_user dependency."""
    app.dependency_overrides[get_current_user] = override_get_current_user
    with TestClient(app) as c:
        yield c
    # Cleanup after the test
    app.dependency_overrides.clear()


# ----------------------- USER ENDPOINT TEST SUITE -----------------------
@pytest.mark.user
def test_create_user(db_session):
    """
    Test the user creation API endpoint.
    """
    # Prepare the user data
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com"
    }

    # Make the request to create a new user via the API
    response = session.post(f"{base_url}/users/create", json=user_data)

    # Assert the response status is OK (201 Created)
    assert response.status_code == 201

    # Retrieve the created user ID from the response
    created_user_id = response.json()["user_id"]

    # Commit the transaction to ensure the user is saved in the database
    db_session.commit()

    # Query the database for the user using the `user_id`
    created_user = db_session.query(User).filter_by(user_id=created_user_id).first()

    # Debugging output to verify the test flow
    if created_user:
        print(f"User ID: {created_user.user_id}, Encrypted Username: {created_user.username}")
        print(f"decrypted username: {decrypt_username(created_user.username)}")

    else:
        print("No user found with the given user_id")

    # Ensure the user was created and fields are properly hashed/encrypted
    assert created_user is not None
    decrypted_username = decrypt_username(created_user.username)
    assert decrypted_username == user_data["username"]
    assert hash_context.verify(user_data["password"], created_user.password)

    # Email is also hashed, so we can't directly verify the value, but we can check that it's hashed
    assert created_user.email != user_data["email"]
    assert created_user.email.startswith("$2b$")  # bcrypt hash prefix
    delete_user(created_user_id,session,base_url)

@pytest.mark.user
def test_get_user_by_id(db_session):
    """
    Test the API endpoint to retrieve a user by their user_id.
    """
    # First, create a user
    user_data = {
        "username": "testuser2",
        "password": "testpassword",
        "email": "testuser2@example.com"
    }
    response = session.post(f"{base_url}/users/create", json=user_data)
    assert response.status_code == 201
    created_user_id = response.json()["user_id"]

    # Commit the transaction to ensure the user is saved in the database
    db_session.commit()

    # Retrieve the user by user_id using the GET endpoint
    get_response = client.get(f"/users/get/{created_user_id}")

    # Assert the response status is OK (200)
    assert get_response.status_code == 200

    # Verify the data in the response
    user = get_response.json()
    assert user["user_id"] == created_user_id

    # Since the email is hashed, we cannot directly compare it to the plain-text value,
    # so we just verify that it's hashed
    assert user["email"].startswith("$2b$")  # Verify it's a bcrypt hash

    # Debugging output to verify the test flow
    # print(f"Retrieved User: {user}")
    assert user["email"].startswith("$2b$")  # Ensure email is hashed
    # print(f"Retrieved User: {user}")
    delete_user(created_user_id, session, base_url)


# Test protected route with mocked authentication
@pytest.mark.user
def test_protected_route_with_mocked_user(client_with_mocked_auth):
    """
    Test a protected route by mocking the authentication process.
    """
    # Simulate calling a protected route that requires authentication
    response = client_with_mocked_auth.get("/auth/protected_route")  # Replace with your actual protected route

    # Assert the request was successful and the mocked user was returned
    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1,
        "username": "mockuser",
        "email": "mockuser@example.com"
    }
