import pytest
from run import create_app

@pytest.fixture(scope='function')  # Use 'function' scope to ensure a fresh app for each test
def app():
    app = create_app()

    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()
