from .database.models import Category, Session, Robot ,get_session
from .enums import RobotState
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class EnergyService:
    @staticmethod
    def add_robot(name: str, token: str, battery_level: float = 100.0, state: str = 'ACTIVE'):
        with get_session() as session:
            try:
                existing_robot = session.query(Robot).filter_by(token=token).first()
                if existing_robot:
                    existing_robot.battery_level = battery_level
                    existing_robot.state = state
                    session.commit()
                    logging.info(f"Updated Robot {name} with token {token}.")
                    return existing_robot
                else:
                    new_robot = Robot(name=name, token=token, battery_level=battery_level, state=state)
                    session.add(new_robot)
                    session.commit()
                    logging.info(f"Robot {name} added to the database successfully.")
                    return new_robot
            except Exception as e:
                logging.error(f"Failed to add/update robot {name}: {e}")
                session.rollback()
                return None


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
        if not isinstance(energy_usage_per_second, (float, int)) or energy_usage_per_second < 0:
            logging.error("Invalid energy usage value.")
            raise ValueError("Energy usage must be a positive float.")

        with get_session() as session:
            if robots is None:
                robots = session.query(Robot).all()

            if not robots:
                logging.warning("No robots found for consumption simulation.")
                return []

            for robot in robots:
                if robot.state == RobotState.ACTIVE.value:
                    robot.consume_energy(energy_usage_per_second)
                    logging.info(f"Robot {robot.id} consumed energy: {energy_usage_per_second}")
            
            session.commit()
        return robots

    @staticmethod
    def add_category(category_name: str, robot_id: int):
        """Add a new category to the database for a specific robot."""
        with get_session() as session:
            try:
                # Assuming you have a Category model
                new_category = Category(name=category_name, robot_id=robot_id)
                session.add(new_category)
                session.commit()
                logging.info(f"Category '{category_name}' added for robot ID {robot_id}.")
                return new_category
            except Exception as e:
                logging.error(f"Failed to add category '{category_name}': {e}")
                session.rollback()
                return None