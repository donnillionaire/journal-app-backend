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

    print(response.status_code, response.json())  # Debugging output

    assert response.status_code == 200
    assert "access_token" in response.json()

# Test User Profile
def test_get_profile_invalid_token():
    """Tests that an invalid token results in a 401 Unauthorized error."""

    headers = {"Authorization": "Bearer invalid_token"}

    response = client.get("/auth/user/profile", headers=headers)

    print(response.status_code, response.json())  # Debugging output

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"







# Create test app
app = FastAPI()
app.include_router(router)
client = TestClient(app)

# Test data
TEST_USER_ID = uuid4()
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "securepassword123"
TEST_FIRST_NAME = "Test"
TEST_LAST_NAME = "User"

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_user():
    user = MagicMock(spec=User)
    user.id = TEST_USER_ID
    user.email = TEST_EMAIL
    user.first_name = TEST_FIRST_NAME
    user.last_name = TEST_LAST_NAME
    user.password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # bcrypt hash of "secret"
    return user

@pytest.fixture
def register_request():
    return {
        "first_name": TEST_FIRST_NAME,
        "last_name": TEST_LAST_NAME,
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }



def test_get_profile_success(mock_db, mock_user):
    # Mock the current user dependency
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    # Call endpoint
    response = client.get("/auth/user/profile")
    
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "User profile retrieved successfully"
    assert data["data"]["email"] == TEST_EMAIL
    assert data["data"]["first_name"] == TEST_FIRST_NAME
    assert data["data"]["last_name"] == TEST_LAST_NAME
    
    # Clean up
    app.dependency_overrides.clear()

