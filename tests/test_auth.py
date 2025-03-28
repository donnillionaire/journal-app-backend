import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.services.auth_service import register_user, login_user
from app.models.model import User
from app.utils.auth import get_current_user
from app.views.auth import RegisterRequest, LoginRequest
import uuid
from app.database import get_db

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from datetime import timedelta
from uuid import uuid4

# Import your router and dependencies
from app.routes.auth import router
from app.models.model import User
from app.views.auth import LoginRequest, RegisterRequest
from app.views.user_schema import UserResponse, UserAPIResponse
from utils.auth import get_current_user
from database import get_db



client = TestClient(app)

# Mock Database Dependency
@pytest.fixture
def mock_db():
    return MagicMock()

# Mock User Data
@pytest.fixture
def mock_user():
    return User(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password="hashedpassword"
    )

def test_register_user(mocker, mock_db):
    # Ensure the mock path is correct
    mock_register = mocker.patch("app.services.auth_service.register_user", return_value={"message": "User registered"})
    
    unique_email = f"john.doe{uuid.uuid4().hex[:6]}@example.com"

    # Make sure your test request matches the expected class
    request_data = {
        "email": unique_email,
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123"
    }

    response = client.post("/auth/user/register", json=request_data)

    print(response.status_code, response.json())  # Debugging output

    assert response.status_code == 201
    
    
def test_login_endpoint():
    """Tests the login endpoint without mocking login_user."""
    request_data = {
        "email": "john.doe@example.com",
        "password": "password123"
    }
    response = client.post("/auth/user/login", json=request_data)
    
    # Debugging output (optional)
    print(response.status_code, response.json())
    
    # Assertions
    assert response.status_code == 200
    response_data = response.json()
    assert "token" in response_data  # Updated key name
    assert response_data["role"] == "USER"  # Optional: Assert role

# Test User Profile
def test_get_profile_invalid_token():
    """Tests that an invalid token results in a 401 Unauthorized error."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/auth/user/profile", headers=headers)
    
    # Debugging output (optional)
    print(response.status_code, response.json())
    
    # Assertions
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token. Please log in again."





    
   
   
   
   
def test_e2e_auth_flow():
    """End-to-End test covering user registration, login, and profile access"""
    unique_email = f"john.doe{uuid.uuid4().hex[:6]}@example.com"

    # Step 1: Register a user
    register_data = {
        "first_name": "E2E",
        "last_name": "User",
        "email": unique_email,
        "password": "strongpassword"
    }
    register_response = client.post("/auth/user/register", json=register_data)
    assert register_response.status_code == 201, register_response.text

    # Step 2: Login with the registered user
    login_data = {
        "email": unique_email,  # Use the same email as during registration
        "password": "strongpassword"
    }
    login_response = client.post("/auth/user/login", json=login_data)
    assert login_response.status_code == 200, login_response.text