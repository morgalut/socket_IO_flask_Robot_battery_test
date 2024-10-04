from enum import Enum

class RobotState(Enum):
    IDLE = "Idle"
    CHARGING = "Charging"
    ACTIVE = "Active"
    ERROR = "Error"

class EnergySource(Enum):
    BATTERY = "Battery"
    GRID = "Grid"
    SOLAR = "Solar"
