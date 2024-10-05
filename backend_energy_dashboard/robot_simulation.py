import random
import time
from app.services import EnergyService  
import requests

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

    def display_battery_status(self):
        """Display the battery status visually."""
        if self.operational_status == "Charging":
            print(f"Charging Robot {self.robot_id}: Battery Level: {self.battery_level}% [CHARGING...]")
        else:
            print(f"Running Robot {self.robot_id}: Battery Level: {self.battery_level}% [RUNNING]")

    def check_battery(self):
        """Check and return the robot's current battery level."""
        if self.battery_level <= 10:
            self.operational_status = "Charging"
            self.current_task = "Charging at station"
            EnergyService.add_robot(name=self.robot_id, token=self.token, battery_level=self.battery_level, state="CHARGING")
        return self.battery_level

    def perform_task(self, task):
        """Simulate the robot performing a task and using battery."""
        if self.battery_level > 10 and self.battery_level < 100:
            self.operational_status = "Working"
            self.current_task = task
            print(f"Robot {self.robot_id} is performing task: {task}")
            self.display_battery_status()  # Display status while working
            self.simulate_battery_usage()

            # After completing the task, add category info
            add_category_to_robot(self.robot_id, "Task Category")  # Specify category name appropriately
        else:
            self.operational_status = "Idle"
            print(f"Robot {self.robot_id} cannot perform the task due to battery status.")
            if self.battery_level >= 100:
                print(f"Robot {self.robot_id} is fully charged and idle.")
            else:
                self.start_charging()

    def start_charging(self):
        """Simulate charging the robot's battery."""
        self.operational_status = "Charging"
        self.current_task = "Charging at station"
        print(f"Robot {self.robot_id} is charging...")
        self.display_battery_status()  # Display status while charging
        while self.battery_level < 100:
            self.battery_level += 5
            time.sleep(1)  # Simulate time passing during charging
            self.display_battery_status()  # Display status while charging
            # Log charging status to database
            EnergyService.add_robot(name=self.robot_id, token=self.token, battery_level=self.battery_level, state="CHARGING")
        self.operational_status = "Idle"
        self.current_task = None
        print(f"Robot {self.robot_id} is fully charged.")

    def simulate_battery_usage(self):
        """Simulate battery depletion while performing tasks."""
        while self.battery_level > 10:
            usage = random.randint(5, 10)
            self.battery_level -= usage
            self.battery_health -= random.uniform(0.1, 0.5)  
            time.sleep(2)  # Simulate time passing during task
            self.display_battery_status()  # Display status while using battery
            if self.battery_level <= 10:
                print(f"Robot {self.robot_id} battery low, needs to recharge.")
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

def create_robot(robot_id, token, battery_capacity=100):
    return Robot(robot_id, token, battery_capacity)


def start_robot_task(robot, task):
    robot.perform_task(task)
    # Update database with the robot's current status after the task is complete
    EnergyService.add_robot(name=robot.robot_id, token=robot.token, battery_level=robot.battery_level, state=robot.operational_status)

def run_system_check(robot):
    robot.check_system()

def add_category_to_robot(robot_id, category_name):
    url = "http://localhost:5000/fleet/add_category"  # Adjust URL as necessary
    payload = {
        "category_name": category_name,
        "robot_id": robot_id
    }
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        print(f"Successfully added category: {category_name} for robot ID: {robot_id}")
    else:
        print(f"Failed to add category: {response.json().get('message')}")

if __name__ == "__main__":
    robots = [
        create_robot(robot_id=101, token="unique_token_101"),
        create_robot(robot_id=102, token="unique_token_102", battery_capacity=100),  # Fully charged
        create_robot(robot_id=103, token="unique_token_103", battery_capacity=50),   # Mid-level battery
        create_robot(robot_id=104, token="unique_token_104", battery_capacity=5),    # Low battery
    ]

    for robot in robots:
        # Add each robot to the database
        EnergyService.add_robot(name=robot.robot_id, token=robot.token, battery_level=robot.battery_level)

    for robot in robots:
        run_system_check(robot)
        # Simulate their tasks based on their initial battery level
        if robot.battery_level <= 10:
            robot.start_charging()
        else:
            start_robot_task(robot, "Performing task")
        run_system_check(robot)
