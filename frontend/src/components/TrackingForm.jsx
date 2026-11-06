// src/components/TrackingForm.jsx
import React from 'react';

const TrackingForm = ({ trackingNumber, setTrackingNumber, onTrack, placeholder }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (trackingNumber.trim()) {
      onTrack(trackingNumber.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <div className="flex">
        {/* Input Field - Updated focus ring to Aramex Red */}
        <input
          type="text"
          value={trackingNumber}
          onChange={(e) => setTrackingNumber(e.target.value)}
          placeholder={placeholder}
          // Changed focus:ring-primary-500 to focus:ring-red-500
          className="flex-1 px-4 py-3 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
        />
        {/* Track Button - Updated to Aramex Red Theme */}
        <button
          type="submit"
          // Changed bg-primary-600 to bg-red-600 and hover:bg-primary-700 to hover:bg-red-700
          className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-r-lg font-medium transition duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
        >
          Track
        </button>
      </div>
    </form>
  );
};

export default TrackingForm;