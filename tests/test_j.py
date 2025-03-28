import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock
from app.main import app

# Import schemas and models
from app.views.journal_schema import JournalCreate, JournalResponse, JournalAPIResponse
from app.models.model import Journal, User
from app.database import get_db  # Import the actual get_db function

# Initialize the TestClient
client = TestClient(app)

@pytest.fixture
def mock_db_session():
    """Fixture to mock the database session."""
    db = MagicMock(spec=Session)
    with patch("app.database.get_db", return_value=db):  # Correct patch path
        yield db

@pytest.fixture
def mock_current_user():
    """Fixture to mock the current authenticated user."""
    user = User(id=1, username="testuser", email="test@example.com")
    with patch("app.utils.auth.get_current_user", return_value=user):  # Correct patch path
        yield user

def test_create_journal_success(mock_db_session, mock_current_user):
    """
    Test successful creation of a journal entry.
    """
    # Arrange: Define the input payload
    journal_data = {
        "title": "My First Journal",
        "content": "This is the content of my first journal entry."
    }
    journal_create = JournalCreate(**journal_data)

    # Mock the database behavior
    mock_journal = Journal(id=1, title=journal_data["title"], content=journal_data["content"], user_id=mock_current_user.id)
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_journal

    # Act: Make the POST request to the endpoint
    response = client.post("/", json=journal_data)

    # Assert: Validate the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "success"
    assert response_data["message"] == "Journal created successfully"
    assert response_data["data"]["title"] == journal_data["title"]
    assert response_data["data"]["content"] == journal_data["content"]

    # Assert: Verify database interactions
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

def test_create_journal_invalid_input(mock_db_session, mock_current_user):
    """
    Test behavior when invalid input is provided.
    """
    # Arrange: Define invalid input payload (missing required fields)
    invalid_journal_data = {
        "content": "This is the content of my first journal entry."  # Missing 'title'
    }

    # Act: Make the POST request to the endpoint
    response = client.post("/", json=invalid_journal_data)

    # Assert: Validate the response
    assert response.status_code == 422  # Unprocessable Entity
    response_data = response.json()
    assert "detail" in response_data
    assert any("title" in error["loc"] for error in response_data["detail"])

def test_create_journal_unauthenticated(mock_db_session):
    """
    Test behavior when the user is not authenticated.
    """
    # Arrange: Mock the current user to be None (unauthenticated)
    with patch("app.utils.auth.get_current_user", return_value=None):  # Correct patch path
        journal_data = {
            "title": "My First Journal",
            "content": "This is the content of my first journal entry."
        }

        # Act: Make the POST request to the endpoint
        response = client.post("/api/journals/", json=journal_data)

        # Assert: Validate the response
        assert response.status_code == 403  # Unauthorized
        response_data = response.json()
        assert response_data["detail"] == "Not authenticated"