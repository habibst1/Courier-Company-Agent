// src/pages/AnonymousChat.jsx
import React, { useState, useEffect } from 'react';
import ChatInterface from '../components/ChatInterface';
import TrackingForm from '../components/TrackingForm';

const AnonymousChat = () => {
  const [trackingNumber, setTrackingNumber] = useState('');
  const [submittedTrackingNumber, setSubmittedTrackingNumber] = useState('');
  const [initialQuestion, setInitialQuestion] = useState('');

  const handleTrack = (number) => {
    setSubmittedTrackingNumber(number);
    // Set an initial question to automatically ask about the tracking
    setInitialQuestion('Give updates about the tracking number');
  };

  // Clear initial question after it's been used
  useEffect(() => {
    if (initialQuestion) {
      const timer = setTimeout(() => {
        setInitialQuestion('');
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [initialQuestion]);

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8"> {/* Increased max-width consistency */}
      {/* Page Header - Slightly increased bottom margin */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-3"> {/* Increased margin below title */}
          Anonymous Tracking
        </h1>
        <p className="text-gray-600">Track packages without logging in using a tracking number</p>
      </div>

      {!submittedTrackingNumber ? (
        // Initial Tracking Form Section - Enhanced Card Styling with Aramex Red Theme
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-8 md:p-10 text-center transition-all duration-300 hover:shadow-lg"> {/* Increased padding, rounded-xl, added transition and hover:shadow-lg */}
          {/* Slightly larger icon container with Aramex Red Theme */}
          <div className="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-6"> {/* bg-primary-100 -> bg-red-50 */}
            <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"> {/* text-primary-600 -> text-red-600 */}
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
            </svg>
          </div>
          {/* Increased headline size and margin */}
          <h2 className="text-2xl font-bold text-gray-900 mb-5"> {/* text-2xl, mb-4->mb-5 */}
            Enter Tracking Number
          </h2>
          <p className="text-gray-600 mb-7"> {/* Increased bottom margin */}
            Provide your package tracking number to get started with tracking
          </p>
          {/* Tracking Form - Pass the placeholder */}
          <TrackingForm
            trackingNumber={trackingNumber}
            setTrackingNumber={setTrackingNumber}
            onTrack={handleTrack}
            placeholder="e.g., TN0001"
          />
        </div>
      ) : (
        // Chat Interface Section - Improved Header and Container with Aramex Red Theme
        <div>
          {/* Tracking Session Header - Enhanced styling and spacing with Aramex Red Theme */}
          <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 bg-white rounded-xl shadow-sm border border-gray-200"> {/* Added padding, rounded-xl, shadow, border, flex-col for mobile stacking */}
            <div>
              {/* Increased font size for tracking number */}
              <h2 className="text-xl font-bold text-gray-900">Tracking: {submittedTrackingNumber}</h2>
              <p className="text-gray-600">Anonymous tracking session</p>
            </div>
            {/* Enhanced "Change" button styling with Aramex Red Theme */}
            <button
              onClick={() => {
                setTrackingNumber('');
                setSubmittedTrackingNumber('');
              }}
              className="text-red-600 hover:text-red-700 hover:bg-red-50 px-4 py-2 rounded-lg text-sm font-medium transition duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2" // text-primary-600 -> text-red-600, hover:text-primary-700 -> hover:text-red-700, hover:bg-primary-50 -> hover:bg-red-50, focus:ring-primary-500 -> focus:ring-red-500
            >
              Change Tracking Number
            </button>
          </div>
          {/* Chat Interface Container - Ensure consistent height and styling */}
          <div className="h-[500px] lg:h-[650px]"> {/* h-96->h-[500px], lg:h-[600px]->lg:h-[650px] */}
            <ChatInterface
              userType="anonymous"
              initialTrackingNumber={submittedTrackingNumber}
              initialQuestion={initialQuestion}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default AnonymousChat;