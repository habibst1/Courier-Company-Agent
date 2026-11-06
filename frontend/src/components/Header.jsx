// src/components/Header.jsx
import React from 'react';
import { Link, useLocation } from 'react-router-dom'; // Import useLocation

const Header = () => {
  const location = useLocation(); // Get current location

  // Function to determine if a link is active
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      {/* Increased py-3 to py-4 for slightly more height */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16"> {/* h-16 is fine, py controls padding */}
          <div className="flex items-center">
            {/* Updated Logo to Aramex Red Theme */}
            <div className="flex-shrink-0">
              <div className="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center"> {/* bg-primary-600 -> bg-red-600 */}
                <span className="text-white font-bold text-xl"> {/* text-lg->text-xl */}
                  C
                </span>
              </div>
            </div>
            <div className="ml-4">
              {/* Adjusted font size for brand name */}
              <h1 className="text-2xl font-bold text-gray-900">CourierTrack AI</h1>
            </div>
          </div>
          {/* Navigation - Improved link styling and added active state with Aramex Red */}
          <nav className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-1"> {/* Reduced space-x-4 to space-x-1 for tighter links */}
              {/* Home Link */}
              <Link
                to="/"
                className={`px-4 py-2 rounded-md text-sm font-medium transition duration-200 ${
                  isActive('/') // Check if active
                    ? 'bg-red-50 text-red-700 border border-red-200' // Active styles: bg-red-50, text-red-700, border-red-200
                    : 'text-gray-600 hover:text-red-600 hover:bg-gray-50' // Default/ Hover styles: hover:text-red-600
                }`}
              >
                Home
              </Link>
              {/* Authenticated Chat Link */}
              <Link
                to="/authenticated"
                className={`px-4 py-2 rounded-md text-sm font-medium transition duration-200 ${
                  isActive('/authenticated')
                    ? 'bg-red-50 text-red-700 border border-red-200' // Active styles
                    : 'text-gray-600 hover:text-red-600 hover:bg-gray-50' // Default/ Hover styles
                }`}
              >
                Customer Service
              </Link>
              {/* Anonymous Tracking Link */}
              <Link
                to="/anonymous"
                className={`px-4 py-2 rounded-md text-sm font-medium transition duration-200 ${
                  isActive('/anonymous')
                    ? 'bg-red-50 text-red-700 border border-red-200' // Active styles
                    : 'text-gray-600 hover:text-red-600 hover:bg-gray-50' // Default/ Hover styles
                }`}
              >
                Anonymous Tracking
              </Link>
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;