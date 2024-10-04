import random
import time
from app.services import EnergyService  

class Robot:
    def __init__(self, robot_id, token, battery_capacity=100):
        self.robot_id = robot_id
        self.token = token  # Unique token for the robot
        self.battery_level = battery_capacity  # In percentage
        self.operational_status = "Idle"  
        self.current_task = None  
        self.location = "Home Base"  
        self.is_operational = True  
        self.battery_health = 100.0  
    
    def check_battery(self):
        """Check and return the robot's current battery level."""
        if self.battery_level <= 10:
            self.operational_status = "Charging"
            self.current_task = "Charging at station"
            # Log this robot in the database with its token
            EnergyService.add_robot(name=self.robot_id, token=self.token, battery_level=self.battery_level, state="CHARGING")
        return self.battery_level

    def perform_task(self, task):
        """Simulate the robot performing a task and using battery."""
        if self.battery_level > 10:
            self.operational_status = "Working"
            self.current_task = task
            print(f"Robot {self.robot_id} is performing task: {task}")
            self.simulate_battery_usage()
        else:
            self.operational_status = "Idle"
            print(f"Robot {self.robot_id} has low battery and cannot perform the task.")
            self.start_charging()

    def start_charging(self):
        """Simulate charging the robot's battery."""
        self.operational_status = "Charging"
        self.current_task = "Charging at station"
        print(f"Robot {self.robot_id} is charging...")
        while self.battery_level < 100:
            self.battery_level += 5
            time.sleep(1)  
            print(f"Battery level: {self.battery_level}%")
        self.operational_status = "Idle"
        self.current_task = None
        print(f"Robot {self.robot_id} is fully charged.")

    def simulate_battery_usage(self):
        """Simulate battery depletion while performing tasks."""
        while self.battery_level > 10:
            self.battery_level -= random.randint(5, 10)
            self.battery_health -= random.uniform(0.1, 0.5)  
            time.sleep(2)  
            print(f"Battery level: {self.battery_level}%, Health: {self.battery_health:.2f}%")
            if self.battery_level <= 10:
                print(f"Robot {self.robot_id} battery low, needs to recharge.")
                # Log low battery status in the database with its token
                EnergyService.add_robot(name=self.robot_id, token=self.token, battery_level=self.battery_level, state="CHARGING")
                self.start_charging()
                break

    def check_system(self):
        """Run a full system check of the robot."""
        print(f"\n--- Running system check for Robot {self.robot_id} ---")
        print(f"Operational Status: {self.operational_status}")
        print(f"Current Task: {self.current_task if self.current_task else 'None'}")
        print(f"Location: {self.location}")
        print(f"Battery Level: {self.battery_level}%")
        print(f"Battery Health: {self.battery_health:.2f}%")
        print(f"System Status: {'Operational' if self.is_operational else 'Faulty'}")
        print("--- System check complete ---\n")

def create_robot(robot_id, token):
    return Robot(robot_id, token)

def start_robot_task(robot, task):
    robot.perform_task(task)

def run_system_check(robot):
    robot.check_system()

if __name__ == "__main__":
    robot1 = create_robot(robot_id=101, token="unique_token_101")  # Example token
    
    # Add the robot to the database
    EnergyService.add_robot(name=robot1.robot_id, token=robot1.token, battery_level=robot1.battery_level)

    run_system_check(robot1)
    start_robot_task(robot1, "Delivering materials to Station B")
    run_system_check(robot1)
