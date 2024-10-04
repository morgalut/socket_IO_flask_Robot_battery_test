import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Robot {
  id: number;
  battery_level: number;
}

interface FleetStatus {
  total_robots: number;
  active: number;
  charging: number;
  battery_health: number;
  fleet: Robot[];
}

const RobotFleetStatus: React.FC = () => {
  const [status, setStatus] = useState<FleetStatus>({ 
    total_robots: 0, 
    active: 0, 
    charging: 0, 
    battery_health: 0, 
    fleet: [] // Set fleet to an empty array initially
  });

  const fetchFleetStatus = async () => {
    try {
      const response = await axios.get('/fleet/status'); // Change to your backend URL
      console.log(response.data); // Log the response to check its structure
      setStatus(response.data);
    } catch (error) {
      console.error("Error fetching fleet status:", error);
    }
  };

  useEffect(() => {
    fetchFleetStatus();
  }, []);

  return (
    <div>
      <h2>Fleet Status</h2>
      <p>Total Robots: {status.total_robots}</p>
      <p>Active Robots: {status.active}</p>
      <p>Charging Robots: {status.charging}</p>
      <p>Average Battery Health: {status.battery_health.toFixed(2)}%</p>
      <h3>Robot Details:</h3>
      <ul>
        {Array.isArray(status.fleet) && status.fleet.length > 0 ? (
          status.fleet.map(robot => (
            <li key={robot.id}>Robot ID: {robot.id}, Battery Level: {robot.battery_level}%</li>
          ))
        ) : (
          <p>No robots available.</p>
        )}
      </ul>
    </div>
  );
};

export default RobotFleetStatus;
