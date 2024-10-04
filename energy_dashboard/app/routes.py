from flask import Blueprint, jsonify, request
from .services import EnergyService

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Welcome to the Energy Dashboard!"

@main.route('/fleet/status', methods=['GET'])
def fleet_status():
    """Returns the current status of the robot fleet."""
    robots = EnergyService.get_all_robots()
    status = EnergyService.get_fleet_status(robots)
    return jsonify(status)

@main.route('/fleet/simulate', methods=['POST'])
def simulate_consumption():
    """Simulates energy consumption for each robot."""
    data = request.get_json()
    usage = data.get('energy_usage', 1.0)
    robots = EnergyService.get_all_robots()
    updated_fleet = EnergyService.simulate_energy_consumption(usage, robots)
    return jsonify([{"id": r.id, "battery_level": r.battery_level, "state": r.state} for r in updated_fleet])

@main.route('/fleet/add_robot', methods=['POST'])
def add_robot_route():
    """Adds a new robot to the fleet."""
    data = request.get_json()
    robot_id = data.get('robot_id')
    battery_level = data.get('battery_level', 100.0)

    # Add robot to the database
    new_robot = EnergyService.add_robot(name=robot_id, battery_level=battery_level)
    if new_robot:
        return jsonify({"message": "Robot added successfully", "robot_id": new_robot.name}), 201
    else:
        return jsonify({"error": "Failed to add robot"}), 400

