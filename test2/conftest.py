import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient

# Test database configuration
# Use SQLite for testing to avoid conflicts with production database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

# Create engine for testing
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create a testing session factory
TestingSessionLocal = sessionmaker(
    autocommit=False,  # Disable auto-commit
    autoflush=False,   # Disable auto-flush
    bind=engine       # Bind to test database engine
)

def override_get_db():
    """
    Override the get_db dependency for testing
    Yields a database session and ensures it's closed after use
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def db():
    """
    Database fixture with session management
    - Creates all tables before test
    - Provides a database session
    - Drops all tables after test
    """
    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)
    
    # Create a new database session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        # Close the session
        db.close()
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    """
    Test client fixture
    - Overrides the database dependency
    - Returns a TestClient for API testing
    """
    # Override the get_db dependency with test database
    app.dependency_overrides[get_db] = override_get_db
    
    # Create and return test client
    return TestClient(app)

@pytest.fixture(scope="function")
def test_user_data():
    """
    Fixture providing sample user registration data
    """
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "password": "StrongPassword123!"
    }

@pytest.fixture(scope="function")
def test_admin_data():
    """
    Fixture providing sample admin registration data
    """
    return {
        "first_name": "Test",
        "last_name": "Admin",
        "email": "testadmin@example.com",
        "password": "AdminPassword123!",
        "role": "ADMIN"
    }