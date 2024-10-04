# tests/test_routes.py
import pytest
from app import create_app

@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()

def test_index(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Energy Dashboard!" in response.data
