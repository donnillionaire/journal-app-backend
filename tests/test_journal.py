import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4
from datetime import datetime, date
from sqlalchemy.orm import Session

# Import your router and dependencies
from app.routes.journal import router
from app.models.model import Journal, User
from app.views.journal_schema import JournalCreate, JournalResponse, JournalListResponse, JournalUpdate
from app.views.user_schema import SummaryResponse
from utils.auth import get_current_user  # Import the actual dependency
from database import get_db  # Import the actual DB dependency

# Create a test app
app = FastAPI()
app.include_router(router)
client = TestClient(app)

# Test data
TEST_USER_ID = uuid4()
TEST_JOURNAL_ID = str(uuid4())
TEST_DATE = date(2023, 1, 1)
TEST_CATEGORY = "Personal"

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_current_user():
    user = MagicMock(spec=User)
    user.id = TEST_USER_ID
    return user

@pytest.fixture
def sample_journal_data():
    return {
        "title": "Test Journal",
        "content": "This is a test journal entry.",
        "journal_category": TEST_CATEGORY,
        "date_of_entry": TEST_DATE.isoformat(),
    }

@pytest.fixture
def sample_journal(sample_journal_data):
    journal = MagicMock(spec=Journal)
    journal.id = TEST_JOURNAL_ID
    journal.user_id = TEST_USER_ID
    journal.title = sample_journal_data["title"]
    journal.content = sample_journal_data["content"]
    journal.journal_category = sample_journal_data["journal_category"]
    journal.date_of_entry = TEST_DATE
    return journal

def test_get_word_frequency_empty(mock_db, mock_current_user):
    # Setup mock
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Mock dependencies
    app.dependency_overrides[get_current_user] = lambda: mock_current_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Call the endpoint
    response = client.get("/api/journals/word-frequency")
    
    # Assertions
    assert response.status_code == 200
    assert response.json() == {"word_frequency": []}
    
    # Clean up
    app.dependency_overrides.clear()

def test_get_word_frequency_with_content(mock_db, mock_current_user):
    # Create test journals
    journal1 = MagicMock(spec=Journal)
    journal1.content = "hello world hello"
    journal2 = MagicMock(spec=Journal)
    journal2.content = "world test"
    
    # Setup mock
    mock_db.query.return_value.filter.return_value.all.return_value = [journal1, journal2]
    
    # Mock dependencies
    app.dependency_overrides[get_current_user] = lambda: mock_current_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Call the endpoint
    response = client.get("/api/journals/word-frequency")
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert len(data["word_frequency"]) > 0
    
    # Clean up
    app.dependency_overrides.clear()

    # Clean up
    app.dependency_overrides.clear()
def test_get_journal_by_category_success(mock_db, mock_current_user, sample_journal):
    # Setup mock
    mock_db.query.return_value.filter.return_value.filter.return_value.order_by.return_value.all.return_value = [sample_journal]
    
    # Mock dependencies
    app.dependency_overrides[get_current_user] = lambda: mock_current_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Call the endpoint
    response = client.get(f"/api/journals/by-category/{TEST_CATEGORY}")
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 1
    
    # Clean up
    app.dependency_overrides.clear()

def test_get_journal_by_category_invalid(mock_db, mock_current_user):
    # Mock dependencies
    app.dependency_overrides[get_current_user] = lambda: mock_current_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Call the endpoint with invalid category
    response = client.get("/api/journals/by-category/InvalidCategory")
    
    # Assertions
    assert response.status_code == 400
    assert "Invalid category" in response.json()["detail"]
    
    # Clean up
    app.dependency_overrides.clear()
    
    
    
    


# Mock dependencies
def override_get_db():
    db = MagicMock()
    return db

def override_get_current_user():
    return User(id=1)  # Mock user with ID 1

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.mark.parametrize("endpoint", [
    "/api/journals/word-frequency",
    "/api/journals/summaries",
    "/api/journals/",
    "/api/journals/123e4567-e89b-12d3-a456-426614174000",
    "/api/journals/by-date/2025-03-27",
    "/api/journals?year=2025",
    "/api/journals/by-category/Personal",
])
def test_unauthorized_access(endpoint):
    """ Test that protected endpoints return 401 when not authenticated """
    app.dependency_overrides.pop(get_current_user, None)

    response = client.get(endpoint)

    assert response.status_code == 401, f"Unexpected response: {response.text}"

@pytest.mark.parametrize("method, endpoint", [
    ("PUT", "/api/journals/123e4567-e89b-12d3-a456-426614174000"),
    ("DELETE", "/api/journals/123e4567-e89b-12d3-a456-426614174000"),
])
def test_unauthorized_modify_or_delete(method, endpoint):
    """ Test that modifying/deleting a journal returns 401 when not authenticated """
    app.dependency_overrides.pop(get_current_user, None)

    if method == "PUT":
        response = client.put(endpoint, json={"title": "Updated", "content": "Updated content"})
    elif method == "DELETE":
        response = client.delete(endpoint)

    assert response.status_code == 401, f"Unexpected response: {response.text}"
