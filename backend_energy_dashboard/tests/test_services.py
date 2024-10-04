from unittest.mock import patch
from app.services import EnergyService
from app.database.models import Robot

@patch('app.services.Session')
def test_get_fleet_status(mock_session):
    """Test the fleet status retrieval."""
    robots = [Robot(id=1, battery_level=100), Robot(id=2, battery_level=50)]
    
    # Mock the query response to return robots
    mock_session.return_value.__enter__.return_value.query.return_value.all.return_value = robots

    status = EnergyService.get_fleet_status()  # Call the method without passing robots
    assert status['total_robots'] == 2  # Expecting two robots
    assert 'battery_health' in status  # Ensure the battery health is included in the response
