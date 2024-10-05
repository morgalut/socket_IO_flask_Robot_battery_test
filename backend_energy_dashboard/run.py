from flask import Flask
from flask_cors import CORS
from config import DevelopmentConfig
from app import socketio
from app.routes import main as main_blueprint
from app.database.models import create_db_engine, init_db

def create_app():
    app = Flask(__name__)

    # Load the configuration from DevelopmentConfig
    app.config.from_object(DevelopmentConfig)

    # Enable CORS for all routes
    CORS(app)

    # Avoid re-registering the blueprint if it's already registered
    if 'main' not in app.blueprints:
        app.register_blueprint(main_blueprint)

    return app

# Create and configure the Flask app
app = create_app()

# Create the database engine and initialize the database
engine = create_db_engine()
init_db(engine)

if __name__ == '__main__':
    # Run the app using socketio for WebSocket support
    socketio.run(app, debug=True)
