import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Import your CSS styles (if any)

const Navbar: React.FC = () => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">Energy Dashboard</Link>
      </div>
      <ul className="navbar-links">
        <li>
          <Link to="/">Fleet Status</Link>
        </li>
        <li>
          <Link to="/simulate">Simulate Consumption</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
