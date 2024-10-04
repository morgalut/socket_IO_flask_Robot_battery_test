from flask_socketio import SocketIO
from energy_dashboard.app.services import EnergyService
from . import create_app

app = create_app()
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    """Send current fleet status to client upon connection."""
    print("Client connected")
    robots = EnergyService.get_all_robots()
    print("Robots retrieved:", robots)  # Debugging robots
    status = EnergyService.get_fleet_status(robots)
    print("Fleet status:", status)  # Debugging fleet status
    socketio.emit('status_update', status)
    
    
@socketio.on('energy_update')
def handle_energy_update(data):
    """Handle real-time energy updates."""
    usage = data.get('energy_usage', 1.0)
    robots = EnergyService.get_all_robots()  # Fetch updated robot data from DB
    updated_fleet = EnergyService.simulate_energy_consumption(energy_usage_per_second=usage, robots=robots)
    socketio.emit('status_update', {
        "fleet": [{"id": r.id, "battery_level": r.battery_level} for r in updated_fleet]
    })
