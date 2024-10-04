// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import RobotFleetStatus from './components/FleetStatus'; // Update import to match the new name
import SimulateConsumption from './components/SimulateConsumption';
import Navbar from './components/Navbar'; 

const App: React.FC = () => {
  return (
    <Router>
      <div>
        <Navbar />
        <h1>Energy Dashboard</h1>
        <Routes>
          <Route path="/" element={<RobotFleetStatus />} /> {/* Updated component reference */}
          <Route path="/simulate" element={<SimulateConsumption />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
