import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.model import User
from app.database import get_db
from app.utils.auth import create_access_token

# Mock database dependency
def override_get_db():
    try:
        db = TestClient(app)
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture
def test_user_data():
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "password": "StrongPassword123!"
    }

@pytest.fixture
def test_admin_data():
    return {
        "first_name": "Test",
        "last_name": "Admin",
        "email": "testadmin@example.com",
        "password": "AdminPassword123!",
        "role": "ADMIN"
    }

def test_user_registration(test_user_data):
    # Test successful user registration
    response = client.post("/auth/user/register", json=test_user_data)
    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert "id" in response.json()["data"]

def test_duplicate_user_registration(test_user_data):
    # First registration
    client.post("/auth/user/register", json=test_user_data)
    
    # Attempt duplicate registration
    response = client.post("/auth/user/register", json=test_user_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_user_login(test_user_data):
    # First, ensure user is registered
    client.post("/auth/user/register", json=test_user_data)
    
    # Test successful login
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/auth/user/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_invalid_login():
    # Test login with incorrect credentials
    invalid_login = {
        "email": "nonexistent@example.com",
        "password": "WrongPassword"
    }
    response = client.post("/auth/user/login", json=invalid_login)
    assert response.status_code == 401

def test_admin_registration(test_admin_data):
    # Test successful admin registration
    response = client.post("/auth/admin/register", json=test_admin_data)
    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert "id" in response.json()["data"]

def test_admin_login(test_admin_data):
    # First, ensure admin is registered
    client.post("/auth/admin/register", json=test_admin_data)
    
    # Test successful admin login
    login_data = {
        "email": test_admin_data["email"],
        "password": test_admin_data["password"]
    }
    response = client.post("/auth/admin/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_user_profile(test_user_data):
    # Register and login user
    client.post("/auth/user/register", json=test_user_data)
    login_response = client.post("/auth/user/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    # Get user profile
    profile_response = client.get("/auth/user/profile", headers={
        "Authorization": f"Bearer {token}"
    })
    assert profile_response.status_code == 200
    assert profile_response.json()["data"]["email"] == test_user_data["email"]

def test_get_admin_profile(test_admin_data):
    # Register and login admin
    client.post("/auth/admin/register", json=test_admin_data)
    login_response = client.post("/auth/admin/login", json={
        "email": test_admin_data["email"],
        "password": test_admin_data["password"]
    })
    token = login_response.json()["access_token"]
    
    # Get admin profile
    profile_response = client.get("/auth/admin/profile", headers={
        "Authorization": f"Bearer {token}"
    })
    assert profile_response.status_code == 200
    assert profile_response.json()["data"]["email"] == test_admin_data["email"]
    assert profile_response.json()["data"]["role"] == "ADMIN"