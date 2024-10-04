from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..enums import RobotState, EnergySource
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Robot(Base):
    __tablename__ = 'robots'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=False)  # Unique token for the robot
    energy_source = Column(String, default=EnergySource.BATTERY.value)
    state = Column(String, default=RobotState.IDLE.value)
    battery_level = Column(Float, default=100.0)  # Percentage

    def consume_energy(self, amount: float) -> None:
        """Simulates energy consumption, updates the robot's state based on battery."""
        if amount < 0:
            raise ValueError("Energy consumption amount must be positive.")

        if self.battery_level - amount > 0:
            self.battery_level -= amount
            self.state = RobotState.ACTIVE.value
        else:
            self.battery_level = 0
            self.state = RobotState.ERROR.value

    def recharge(self) -> None:
        """Simulates recharging the robot."""
        if self.state == RobotState.ERROR.value:
            raise RuntimeError("Robot is in ERROR state. Cannot recharge without repair.")
        
        self.battery_level = 100.0
        self.state = RobotState.CHARGING.value

    def repair(self) -> None:
        """Simulates robot repair and reinitialization."""
        if self.state == RobotState.ERROR.value:
            self.state = RobotState.IDLE.value
            self.battery_level = 100.0
        else:
            raise RuntimeError("Robot is not in ERROR state. No repair needed.")

# Database connection setup
def create_db_engine(db_path: str = 'sqlite:///robots.db'):
    """Creates and returns a SQLAlchemy engine."""
    return create_engine(db_path)

def init_db(engine):
    """Initializes the database, creating necessary tables."""
    Base.metadata.create_all(engine)

# Create a session maker for interacting with the database
Session = sessionmaker(bind=create_db_engine())

# Utility function to create sessions
def get_session() -> SQLAlchemySession:
    """Gets a new session for database interaction.""" 
    return Session()
