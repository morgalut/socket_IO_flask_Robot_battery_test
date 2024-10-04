from flask import Flask
from config import DevelopmentConfig
from app import socketio
from app.routes import main as main_blueprint  # Correct import
from robot_simulation import create_robot, start_robot_task, run_system_check
from app.database.models import create_db_engine, init_db  # Import your database setup functions
import uuid  # Importing the uuid module for generating unique tokens

def create_app():
    app = Flask(__name__)
    
    # Load the configuration from DevelopmentConfig
    app.config.from_object(DevelopmentConfig)
    
    # Avoid re-registering the blueprint if it's already registered
    if 'main' not in [bp.name for bp in app.blueprints.values()]:
        app.register_blueprint(main_blueprint)

    return app

# Create and configure the Flask app
app = create_app()

# Create the database engine and initialize the database
engine = create_db_engine()  # Create the database engine
init_db(engine)  # Initialize the database

# Function to run the robot simulation tasks
def run_robot_simulation():
    # Generate a unique token
    unique_token = str(uuid.uuid4())  # Generates a random UUID
    
    # Create the robot with a unique ID and token
    robot1 = create_robot(robot_id=101, token=unique_token)
    
    # Run an initial system check
    run_system_check(robot1)

    # Start a task for the robot
    task_name = "Transport goods to storage"
    start_robot_task(robot1, task_name)

    # Run another system check after completing the task
    run_system_check(robot1)

if __name__ == '__main__':
    # Run the robot simulation in a separate thread or before the app starts
    run_robot_simulation()
    
    # Run the app using socketio for WebSocket support
    socketio.run(app, debug=True)
