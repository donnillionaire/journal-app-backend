import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user():
    """Ensure a new user can register successfully."""
    unique_email = f"testuser{uuid.uuid4().hex[:6]}@example.com"
    register_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": unique_email,
        "password": "securepassword"
    }
    response = client.post("/auth/user/register", json=register_data)
    assert response.status_code == 201, response.text
    assert "message" in response.json()
    assert response.json()["message"] == "User registered successfully"


def test_login_user():
    """Ensure login works with valid credentials."""
    unique_email = f"testuser{uuid.uuid4().hex[:6]}@example.com"
    register_data = {
        "first_name": "Login",
        "last_name": "Tester",
        "email": unique_email,
        "password": "testpassword"
    }
    register_response = client.post("/auth/user/register", json=register_data)
    assert register_response.status_code == 201, register_response.text
    
    login_data = {
        "email": unique_email,
        "password": "testpassword"
    }
    response = client.post("/auth/user/login", json=login_data)
    assert response.status_code == 200, response.text
    json_response = response.json()
    assert "token" in json_response, f"Unexpected response: {json_response}"
    

def test_get_profile():
    """Ensure profile retrieval works with a valid token."""
    unique_email = f"profileuser{uuid.uuid4().hex[:6]}@example.com"
    register_data = {
        "first_name": "Profile",
        "last_name": "User",
        "email": unique_email,
        "password": "profilepassword"
    }
    client.post("/auth/user/register", json=register_data)
    
    login_data = {
        "email": unique_email,
        "password": "profilepassword"
    }
    login_response = client.post("/auth/user/login", json=login_data)
    assert login_response.status_code == 200, login_response.text
    json_response = login_response.json()
    
    token = json_response.get("token")
    assert token, f"Token missing in response: {json_response}"
    
    headers = {"Authorization": f"Bearer {token}"}
    profile_response = client.get("/auth/user/profile", headers=headers)
    assert profile_response.status_code == 200, profile_response.text


def test_e2e_auth_flow():
    """End-to-End test covering registration, login, and profile access."""
    unique_email = f"e2euser{uuid.uuid4().hex[:6]}@example.com"
    register_data = {
        "first_name": "E2E",
        "last_name": "Tester",
        "email": unique_email,
        "password": "e2epassword"
    }
    response = client.post("/auth/user/register", json=register_data)
    assert response.status_code == 201, response.text
    
    login_data = {"email": unique_email, "password": "e2epassword"}
    login_response = client.post("/auth/user/login", json=login_data)
    assert login_response.status_code == 200, login_response.text
    json_response = login_response.json()
    
    token = json_response.get("token")
    assert token, f"Token missing in response: {json_response}"
    
    headers = {"Authorization": f"Bearer {token}"}
    profile_response = client.get("/auth/user/profile", headers=headers)
    assert profile_response.status_code == 200, profile_response.text
