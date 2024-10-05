from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from ..enums import RobotState, EnergySource
from sqlalchemy.orm import Session as SQLAlchemySession

# Base class for declarative models
Base = declarative_base()

class Robot(Base):
    """Represents a robot in the fleet."""
    __tablename__ = 'robots'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    token = Column(String, unique=True, nullable=False, index=True)  # Unique token for the robot
    energy_source = Column(String, default=EnergySource.BATTERY.value)
    state = Column(String, default=RobotState.IDLE.value)
    battery_level = Column(Float, default=100.0)  # Battery level percentage

    # Relationship with Category
    categories = relationship('Category', back_populates='robot', cascade='all, delete-orphan')

    def consume_energy(self, amount: float) -> None:
        """Simulates energy consumption and updates the robot's state."""
        if amount < 0:
            raise ValueError("Energy consumption amount must be positive.")

        self.battery_level = max(0, self.battery_level - amount)
        self.state = RobotState.ACTIVE.value if self.battery_level > 0 else RobotState.ERROR.value

    def recharge(self) -> None:
        """Recharges the robot's battery to full."""
        if self.state == RobotState.ERROR.value:
            raise RuntimeError("Robot is in ERROR state. Cannot recharge without repair.")
        
        self.battery_level = 100.0
        self.state = RobotState.CHARGING.value

    def repair(self) -> None:
        """Repairs the robot, restoring it to an operational state."""
        if self.state == RobotState.ERROR.value:
            self.state = RobotState.IDLE.value
            self.battery_level = 100.0
        else:
            raise RuntimeError("Robot is not in ERROR state. No repair needed.")

    def battery_status(self) -> str:
        """Returns the battery status as a string."""
        return f"Battery level: {self.battery_level:.2f}%"

    def __repr__(self) -> str:
        """String representation of the Robot object."""
        return (f"<Robot(id={self.id}, name={self.name}, token={self.token}, "
                f"energy_source={self.energy_source}, state={self.state}, "
                f"battery_level={self.battery_level:.2f}%)>")

class Category(Base):
    """Represents a category associated with a robot."""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    robot_id = Column(Integer, ForeignKey('robots.id'), nullable=False)

    robot = relationship('Robot', back_populates='categories')

# Database connection setup
def create_db_engine(db_path: str = 'sqlite:///robots.db') -> SQLAlchemySession:
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
