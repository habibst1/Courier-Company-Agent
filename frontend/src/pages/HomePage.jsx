// src/pages/HomePage.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import { mockShipments } from '../mock/mockData';

const HomePage = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16 mt-8">
        {/* Adjusted for Aramex red and modern font weights */}
        <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold text-gray-900 leading-tight mb-6">
          AI-Powered <span className="text-red-600">Courier Tracking</span> {/* Changed to red-600 */}
        </h1>
        <p className="text-lg md:text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
          Track your shipments with natural language queries. Ask questions like "Where is my package?" or "Show me recent deliveries."
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          {/* Authenticated Chat Button - Aramex Red Theme */}
          <Link
            to="/authenticated"
            className="bg-red-600 hover:bg-red-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
          >
            Customer Service Chat
          </Link>
          {/* Anonymous Tracking Button - Outlined Aramex Red Theme */}
          <Link
            to="/anonymous"
            className="bg-white hover:bg-gray-50 text-red-600 border-2 border-red-600 px-8 py-4 rounded-xl font-semibold text-lg transition duration-300 shadow hover:shadow-md transform hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
          >
            Anonymous Tracking
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div className="grid md:grid-cols-3 gap-8 mb-16">
        {/* Feature Cards - Updated with Aramex red accents and modern shadows */}
        <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200 transition duration-300 hover:shadow-lg">
          <div className="w-14 h-14 bg-red-50 rounded-xl flex items-center justify-center mb-5"> {/* Light red background */}
            {/* Updated icon color to Aramex red */}
            <svg className="w-7 h-7 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-3">
            Secure Tracking
          </h3>
          <p className="text-gray-600">
            Authenticated users can access their complete shipment history with full privacy protection.
          </p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200 transition duration-300 hover:shadow-lg">
          <div className="w-14 h-14 bg-red-50 rounded-xl flex items-center justify-center mb-5">
            <svg className="w-7 h-7 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-3">
            Natural Language
          </h3>
          <p className="text-gray-600">
            Ask questions in plain English and get instant, accurate responses about your shipments.
          </p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200 transition duration-300 hover:shadow-lg">
          <div className="w-14 h-14 bg-red-50 rounded-xl flex items-center justify-center mb-5">
            <svg className="w-7 h-7 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-3">
            Instant Results
          </h3>
          <p className="text-gray-600">
            Get real-time updates and tracking information without navigating complex menus.
          </p>
        </div>
      </div>

      {/* Demo Shipments */}
      <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6 mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Sample Shipments</h2>
        <div className="space-y-4">
          {mockShipments.map((shipment) => (
            <div
              key={shipment.id}
              className="flex flex-col sm:flex-row sm:items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition duration-200 shadow-sm hover:shadow"
            >
              <div className="mb-3 sm:mb-0">
                <div className="flex flex-wrap items-center gap-2">
                  {/* Tracking number in bold */}
                  <span className="font-semibold text-gray-900">{shipment.tracking_number}</span>
                  {/* Status badge with Aramex-inspired colors */}
                  <span className={`px-3 py-1 text-xs font-medium rounded-full ${
                    shipment.status === 'Delivered'
                      ? 'bg-green-100 text-green-800'
                      : shipment.status === 'In Transit'
                      ? 'bg-blue-100 text-blue-800' // Example for In Transit
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {shipment.status}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mt-2">
                  {shipment.origin} → {shipment.destination}
                </p>
              </div>
              <div className="text-left sm:text-right">
                <p className="text-sm text-gray-600">Expected: {shipment.expected_delivery}</p>
                <p className="text-sm text-gray-600">{shipment.weight}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default HomePage;