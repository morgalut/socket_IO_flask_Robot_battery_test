from flask import Blueprint, Flask
from flask_socketio import SocketIO
from config import Config
from .database.models import create_db_engine, init_db, Session
from .routes import main as main_blueprint  # Use relative import

# Initialize Flask and SocketIO
app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app)

def create_app():
    """Create and configure the Flask app."""
    
    # Create database engine
    engine = create_db_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    
    # Initialize the database
    init_db(engine)

    # Bind the session to the engine
    Session.configure(bind=engine)

    # Register the blueprint correctly
    app.register_blueprint(main_blueprint)

    return app
