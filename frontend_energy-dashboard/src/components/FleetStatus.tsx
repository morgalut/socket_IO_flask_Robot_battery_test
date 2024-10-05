import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Robot {
  id: number;
  battery_level: number;
  is_charged: boolean;
  is_working: boolean;
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
    fleet: [],
  });
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch fleet status from the API
  const fetchFleetStatus = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/fleet/status');
      console.log("API Response:", response.data); // Log the API response for debugging

      // Ensure that the fleet data exists and update state
      const fleetData = response.data?.fleet || [];
      setStatus({
        total_robots: response.data.total_robots,
        active: response.data.active,
        charging: response.data.charging,
        battery_health: response.data.battery_health,
        fleet: fleetData,
      });
      setError(null);
    } catch (error) {
      setError("Error fetching fleet status. Please try again later.");
      console.error("Error fetching fleet status:", error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch fleet status on component mount and every 5 seconds
  useEffect(() => {
    fetchFleetStatus();
    const intervalId = setInterval(fetchFleetStatus, 5000);

    return () => clearInterval(intervalId); // Cleanup interval on component unmount
  }, []);

  // Compute robots' status
  const chargedRobots = status.fleet.filter((robot) => robot.is_charged);
  const workingRobots = status.fleet.filter((robot) => robot.is_working);
  const chargingRobots = status.fleet.filter(
    (robot) => !robot.is_working && robot.battery_level < 100
  );

  return (
    <div>
      <h2>Fleet Status</h2>
      {loading ? (
        <p>Loading fleet status...</p>
      ) : error ? (
        <p className="error">{error}</p>
      ) : (
        <>
          <p>Total Robots: {status.total_robots}</p>
          <p>Active Robots: {status.active}</p>
          <p>Charging Robots: {chargingRobots.length}</p>
          <p>Average Battery Health: {status.battery_health.toFixed(2)}%</p>

          {/* Display All Robots */}
          <h3>All Robots:</h3>
          <RobotList robots={status.fleet} />

          {/* Display Charged Robots */}
          <h3>Charged Robots:</h3>
          <RobotList robots={chargedRobots} />

          {/* Display Working Robots */}
          <h3>Working Robots:</h3>
          <RobotList robots={workingRobots} />

          {/* Display Charging Robots */}
          <h3>Charging Robots:</h3>
          <RobotList robots={chargingRobots} />
        </>
      )}
    </div>
  );
};

// Separate component for displaying robot details
const RobotList: React.FC<{ robots: Robot[] }> = ({ robots }) => {
  return (
    <div className="robot-container">
      {robots.length > 0 ? (
        robots.map((robot) => (
          <div key={robot.id} className="robot-card">
            <h4>Robot ID: {robot.id}</h4>
            <p>Battery Level: {robot.battery_level}%</p>
            <p>
              Status: {robot.is_charged ? 'Charged' : 'Not Charged'},{' '}
              {robot.is_working ? 'Working' : 'Idle'}
            </p>
          </div>
        ))
      ) : (
        <p>No robots available.</p>
      )}
    </div>
  );
};

export default RobotFleetStatus;
