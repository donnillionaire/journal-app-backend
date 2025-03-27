from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app  # Ensure this imports the FastAPI app correctly
from app.database import get_db
from app.models.model import Base
from app.views.auth import RegisterRequest, LoginRequest

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_login_user():
    mock_data = {"email": "test@example.com", "password": "testpassword"}
    response = client.post("/auth/user/login", json=mock_data)
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_get_profile():
    login_data = {"email": "test@example.com", "password": "testpassword"}
    login_response = client.post("/auth/user/login", json=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/user/profile", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "data" in response.json()




def test_e2e_auth_flow():
    """End-to-End test covering user registration, login, and profile access"""

    # Step 1: Register a user
    register_data = {
        "first_name": "E2E",
        "last_name": "User",
        "email": "e2e@example.com",
        "password": "strongpassword"
    }
    register_response = client.post("/auth/user/register", json=register_data)
    assert register_response.status_code == 201, register_response.text

    # Step 2: Login with the registered user
    login_data = {
        "email": "e2e@example.com",
        "password": "strongpassword"
    }
    login_response = client.post("/auth/user/login", json=login_data)
    assert login_response.status_code == 200, login_response.text
    assert "access_token" in login_response.json()

    # Extract token
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Access protected profile route
    profile_response = client.get("/auth/user/profile", headers=headers)
    assert profile_response.status_code == 200, profile_response.text
    assert profile_response.json()["status"] == "success"
    assert profile_response.json()["data"]["email"] == "e2e@example.com"
