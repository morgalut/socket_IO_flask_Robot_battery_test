 
### Project Overview

The **Energy Monitoring Dashboard** aims to provide real-time insights into the energy consumption of a fleet of autonomous robots. This project will help in monitoring the operational efficiency of these robots, managing their energy usage, and ensuring they remain functional without running out of power.

### Project Structure

Here's a breakdown of the project structure, along with a description of each file's role:

```
energy_dashboard/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── enums.py
│   ├── services.py
│   ├── routes.py
├── config.py
├── run.py
├── requirements.txt
├── robots.db

```

### File Descriptions

1. **`app/__init__.py`**:
   - Initializes the Flask application and sets up the application context.
   - Imports necessary modules, initializes extensions (like database connections), and registers blueprints (if applicable).

2. **`app/models.py`**:
   - Contains the data models for the application.
   - Defines classes that represent the `Robot` and its attributes (like `battery_level`, `state`, etc.).
   - If using a database (like SQLAlchemy), this is where you define the ORM (Object Relational Mapping) models.

3. **`app/enums.py`**:
   - Defines enumerations (enums) that categorize various states and actions within the application.
   - For instance, the `RobotState` enum can define possible states of a robot (like `ACTIVE`, `CHARGING`, and `IDLE`).

4. **`app/services.py`**:
   - Contains the business logic for managing the fleet of robots.
   - Includes functions for calculating the overall fleet status (e.g., total robots, active robots, battery health) and simulating energy consumption.

5. **`app/routes.py`**:
   - Defines the API endpoints for your application.
   - Sets up routes (e.g., `/status`, `/simulate`) that correspond to HTTP methods (GET, POST) to handle requests from the front end or other clients.

6. **`config.py`**:
   - Holds configuration settings for the Flask application.
   - Defines settings like the database URI, secret key, and debug mode.

7. **`run.py`**:
   - Serves as the entry point for your application.
   - Initializes the Flask application and runs the development server.

8. **`requirements.txt`**:
   - Lists all dependencies and libraries needed for your project, including Flask and any other packages you are using.
   - You can install all required packages in a virtual environment using `pip install -r requirements.txt`.

### Setting Up a Virtual Environment

To set up a virtual environment for this project, follow these steps:

1. **Install `virtualenv`** (if not already installed):
   ```bash
   pip install virtualenv
   ```

2. **Create a virtual environment**:
   ```bash
   cd capow\energy_dashboard
   python -m virtualenv env 
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source env\Scripts\activate
     ```

4. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

### Functionality of the Project

- **Monitoring Fleet Status**: The dashboard will allow users to query the overall status of the robot fleet, including the number of active robots, those charging, and average battery health.

- **Simulating Energy Consumption**: The service will simulate how energy is consumed by the robots based on their activities and provide updated statuses in real time.

- **Real-Time Data Handling**: The backend handles the logic, and the data will be sent to the frontend via APIs, utilizing WebSocket or similar technologies for real-time updates.

### Conclusion

This project combines Python's Flask framework with OOP principles, allowing for organized, maintainable code that adheres to best practices. The design promotes separation of concerns, ensuring that models, services, and routes are distinct and focused on their responsibilities. This makes it easier to expand the project in the future, whether by adding more features or integrating with a frontend application for visualization and interaction.


