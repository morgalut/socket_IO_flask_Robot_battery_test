import pytest
import time
from flask_socketio import SocketIOTestClient
from app import create_app, socketio
from app.services import EnergyService
from unittest import mock

@pytest.fixture
def socket_client(app):
    """Fixture to create a WebSocket client for testing."""
    app.config['TESTING'] = True
    client = socketio.test_client(app)
    yield client
    client.disconnect()

def test_socket_connect(socket_client):
    """Test if the socket client can successfully connect."""
    assert socket_client.is_connected(), "Socket client failed to connect."

def test_fleet_status(socket_client):
    """Test the fleet status WebSocket event upon connection."""
    with mock.patch.object(EnergyService, 'get_all_robots', return_value=[]):
        
        # Connect the WebSocket client
        socket_client.connect()
        assert socket_client.is_connected(), "Socket client failed to connect."

        # Increase sleep time to allow status update to be received
        time.sleep(5)

        # Fetch received messages
        received = socket_client.get_received()
        print("Received messages:", received)

        # Assert that a 'status_update' message was received
        assert any(msg['name'] == 'status_update' for msg in received), "No 'status_update' received"

        # Check that the received status is as expected for an empty fleet
        for msg in received:
            if msg['name'] == 'status_update':
                data = msg['args'][0]
                assert data['total_robots'] == 0, "Total robots should be 0"
                assert data['active'] == 0, "Active robots should be 0"
                assert data['charging'] == 0, "Charging robots should be 0"
                assert data['battery_health'] == 0.0, "Battery health should be 0.0"
