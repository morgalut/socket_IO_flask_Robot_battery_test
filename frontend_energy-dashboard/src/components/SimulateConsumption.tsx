// src/components/SimulateConsumption.tsx
import React, { useState } from 'react';
import axios from 'axios';

const SimulateConsumption: React.FC = () => {
  const [energyUsage, setEnergyUsage] = useState<number>(1);

  const handleSimulation = async () => {
    try {
      await axios.post('/fleet/simulate', { energy_usage: energyUsage });
      alert('Simulation started');
    } catch (error) {
      console.error("Error simulating consumption:", error);
    }
  };

  return (
    <div>
      <h2>Simulate Energy Consumption</h2>
      <input
        type="number"
        value={energyUsage}
        onChange={(e) => setEnergyUsage(Number(e.target.value))}
      />
      <button onClick={handleSimulation}>Simulate</button>
    </div>
  );
};

export default SimulateConsumption;
