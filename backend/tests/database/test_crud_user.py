import pytest
from sqlalchemy.orm import Session
from app.crud.user import (
    get_user,
    get_user_by_username,
    create_user,
    update_user,
    delete_user,
    verify_password,
    decrypt
)
from app.schemas.user import UserCreate, UserUpdate
from app.db.session import SessionLocal
from fastapi.exceptions import HTTPException
from cryptography.fernet import Fernet
import os

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
fernet = Fernet(ENCRYPTION_KEY)


def encrypt_username(username: str) -> str:
    return fernet.encrypt(username.encode()).decode()


mock_user_data = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testpassword",
    "role_id": 1
}


@pytest.fixture
def test_db_session():
    """Fixture to provide a database session for testing"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_user(test_db_session: Session):
    """Test creating a new user."""
    user_in = UserCreate(**mock_user_data)
    created_user = create_user(test_db_session, user_in)

    assert created_user.username != mock_user_data["username"]
    assert created_user.email != mock_user_data["email"]

    fetched_user = get_user(test_db_session, created_user.user_id)
    assert decrypt(fetched_user.username) == mock_user_data["username"]
    assert verify_password(mock_user_data["password"], fetched_user.password)
    delete_user(test_db_session, created_user.user_id)


def test_get_user(test_db_session: Session):
    """Test retrieving a user by ID."""
    user_in = UserCreate(**mock_user_data)
    created_user = create_user(test_db_session, user_in)
    fetched_user = get_user(test_db_session, created_user.user_id)
    assert fetched_user.user_id == created_user.user_id
    delete_user(test_db_session, created_user.user_id)


def test_update_user(test_db_session: Session):
    """Test updating user information."""
    user_in = UserCreate(**mock_user_data)
    created_user = create_user(test_db_session, user_in)

    update_data = UserUpdate(username="updateduser", email="updatedemail@example.com", password="newpassword")
    updated_user = update_user(test_db_session, created_user.user_id, update_data)

    decrypted_username = decrypt(updated_user.username)
    assert decrypted_username == "updateduser"

    assert updated_user.email is not None and updated_user.email != ""

    assert verify_password("newpassword", updated_user.password)
    delete_user(test_db_session, created_user.user_id)


def test_delete_user(test_db_session: Session):
    """Test deleting a user."""
    user_in = UserCreate(**mock_user_data)
    created_user = create_user(test_db_session, user_in)

    deleted_user = delete_user(test_db_session, created_user.user_id)
    assert deleted_user.user_id == created_user.user_id

    with pytest.raises(HTTPException) as exc_info:
        get_user(test_db_session, created_user.user_id)
    assert exc_info.value.status_code == 404


def test_get_user_not_found(test_db_session: Session):
    """Test error handling when user is not found."""
    with pytest.raises(HTTPException) as exc_info:
        get_user(test_db_session, user_id=9999)
    assert exc_info.value.status_code == 404


def test_get_user_by_username_not_found(test_db_session: Session):
    """Test error handling for non-existent username."""
    user = get_user_by_username(test_db_session, encrypt_username("nonexistentuser"))
    assert user is None


def test_delete_user_not_found(test_db_session: Session):
    """Test error handling when trying to delete a non-existent user."""
    with pytest.raises(HTTPException) as exc_info:
        delete_user(test_db_session, user_id=9999)
    assert exc_info.value.status_code == 404
