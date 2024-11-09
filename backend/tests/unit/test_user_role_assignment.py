# # tests/unit/test_user_role_assignment.py

# import pytest
# import time
# from fastapi.testclient import TestClient
# from app.main import app
# from app.db.session import get_db, SessionLocal
# from app.models.role import Role
# from app.models.user import User
# from tests.integration.tools.get_cookie import get_cookie
# from tests.integration.tools.base_url import base_url

# client = TestClient(app)
# session = get_cookie()

# def override_get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# def unique_username(base="testuser"):
#     """Helper function to generate a unique username."""
#     return f"{base}_{int(time.time())}"

# @pytest.fixture
# def cleanup_user():
#     """Fixture to create a user and delete it after the test."""
#     user_ids = []

#     def _create_user(user_data):
#         response = session.post(f"{base_url}/users/create", json=user_data)
#         assert response.status_code == 201
#         user_id = response.json()["user_id"]
#         user_ids.append(user_id)
#         return user_id

#     yield _create_user

#     # Cleanup: delete created users after the test
#     for user_id in user_ids:
#         session.delete(f"{base_url}/users/delete/{user_id}")

# def test_assign_role_to_user(cleanup_user):
#     # Create a user with a unique username
#     user_data = {
#         "username": unique_username(),
#         "email": f"{unique_username()}@example.com",
#         "password": "password123",
#     }
#     user_id = cleanup_user(user_data)

#     # Assign "Professor" role to the user
#     response = session.put(f"{base_url}/users/update-role/{user_id}", json={"role_name": "Professor"})
#     assert response.status_code == 200
#     assert response.json()["role_id"] == get_role_id("Professor")

#     # Change role to "GradStudent"
#     response = session.put(f"{base_url}/users/update-role/{user_id}", json={"role_name": "GradStudent"})
#     assert response.status_code == 200
#     assert response.json()["role_id"] == get_role_id("GradStudent")

# def get_role_id(role_name):
#     """Helper function to get the role ID by name"""
#     db = SessionLocal()
#     role = db.query(Role).filter(Role.role_name == role_name).first()
#     db.close()
#     return role.role_id if role else None