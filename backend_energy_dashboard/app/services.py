from .database.models import Session, Robot
from .enums import RobotState
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class EnergyService:
    @staticmethod
    def add_robot(name: str, token: str, battery_level: float = 100.0, state: str = 'ACTIVE'):
        """Add a new robot to the fleet or update an existing robot based on token."""
        with Session() as session:
            try:
                # Check if the robot already exists by token
                existing_robot = session.query(Robot).filter_by(token=token).first()
                if existing_robot:
                    # Update existing robot's data
                    existing_robot.battery_level = battery_level
                    existing_robot.state = state
                    logging.info(f"Updated Robot {name} with token {token} in the database.")
                else:
                    # Create a new robot if it does not exist
                    new_robot = Robot(name=name, token=token, battery_level=battery_level, state=state)
                    session.add(new_robot)
                    logging.info(f"Robot {name} added to the database successfully with token {token}.")
                
                session.commit()
            except Exception as e:
                logging.error(f"Failed to add/update robot {name}: {e}")
                session.rollback()  # Rollback the session in case of error

    @staticmethod
    def get_all_robots() -> list[Robot]:
        """Retrieve all robots from the database."""
        with Session() as session:
            robots = session.query(Robot).all()
        return robots

    @staticmethod
    def get_fleet_status(robots: list[Robot] = None) -> dict:
        """Returns the overall energy status of the fleet."""
        if robots is None:  # Fetch robots from the DB if not provided
            with Session() as session:
                robots = session.query(Robot).all()

        if not robots:
            return {
                "total_robots": 0,
                "active": 0,
                "charging": 0,
                "battery_health": 0.0
            }

        battery_levels = [robot.battery_level for robot in robots]
        active_count = sum(1 for robot in robots if robot.state == RobotState.ACTIVE.value)
        charging_count = sum(1 for robot in robots if robot.state == RobotState.CHARGING.value)

        return {
            "total_robots": len(robots),
            "active": active_count,
            "charging": charging_count,
            "battery_health": np.mean(battery_levels)  # Average battery level of the fleet
        }

    @staticmethod
    def simulate_energy_consumption(energy_usage_per_second: float, robots: list[Robot] = None) -> list[Robot]:
        """Simulates energy consumption for each robot in the fleet."""
        if not isinstance(energy_usage_per_second, (float, int)) or energy_usage_per_second < 0:
            logging.error("Invalid energy usage value: must be a positive float.")
            raise ValueError("Energy usage must be a positive float.")

        with Session() as session:
            if robots is None:  # Fetch fleet if no robots are provided
                robots = session.query(Robot).all()

            if not robots:
                logging.warning("No robots found in the fleet for consumption simulation.")
                return []

            for robot in robots:
                if robot.state == RobotState.ACTIVE.value:
                    robot.consume_energy(energy_usage_per_second)
                    logging.info(f"Robot {robot.id} consumed energy: {energy_usage_per_second}")

            session.commit()
        return robots
