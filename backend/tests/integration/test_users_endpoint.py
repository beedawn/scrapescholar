# tests/unit/test_user.py
# need to test /users/create and ensure it updates the db with the new user and provides requested  information
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app  # Import the FastAPI app
from app.models.user import User
from app.models.search import Search
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from app.db.session import SessionLocal
import os
import time
import random
import string

# Initialize TestClient
client = TestClient(app)

# Load environment variables
load_dotenv()
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

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
    return fernet.decrypt(encrypted_username.encode()).decode()

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
    response = client.post("/users/create", json=user_data)

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
    response = client.post("/users/create", json=user_data)
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
    print(f"Retrieved User: {user}")
    assert user["email"].startswith("$2b$")  # Ensure email is hashed
    print(f"Retrieved User: {user}") 