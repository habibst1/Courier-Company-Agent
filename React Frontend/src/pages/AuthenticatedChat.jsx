// src/pages/AuthenticatedChat.jsx
import React from 'react'; // Removed unused useState
import ChatInterface from '../components/ChatInterface';
import { mockUser } from '../mock/mockData';

const AuthenticatedChat = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        {/* Adjusted title color to use gray-900 for consistency */}
        <h1 className="text-3xl font-bold text-gray-900 mb-3">
          Customer Service Chat
        </h1>
        {/* Adjusted description color */}
        <p className="text-gray-600">Chat with our AI assistant using your account credentials</p>
      </div>
      <div className="grid lg:grid-cols-4 gap-6">
        {/* User Info Sidebar - Updated with Aramex Red Theme */}
        <div className="lg:col-span-1">
          {/* Improved sticky behavior and container styling with Aramex colors */}
          <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6 sticky top-6 transition-all duration-300 hover:shadow-lg">
            <div className="flex items-center mb-5">
              {/* Avatar container with Aramex red background */}
              <div className="w-14 h-14 bg-red-50 rounded-full flex items-center justify-center flex-shrink-0"> {/* bg-primary-100 -> bg-red-50 */}
                {/* Initials in Aramex red */}
                <span className="text-red-600 font-bold text-xl"> {/* text-primary-600 -> text-red-600 */}
                  {mockUser.name.charAt(0)}
                </span>
              </div>
              <div className="ml-4 overflow-hidden">
                {/* User name with bold font */}
                <h3 className="font-bold text-gray-900 truncate">
                  {mockUser.name}
                </h3>
                {/* User ID */}
                <p className="text-sm text-gray-600 truncate">User #{mockUser.id}</p>
              </div>
            </div>
            {/* User Details - Improved spacing and typography */}
            <div className="space-y-4">
              <div>
                {/* Label styling with uppercase and tracking */}
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
                  Email
                </p>
                {/* User email */}
                <p className="text-gray-900 truncate">{mockUser.email}</p>
              </div>
              <div>
                {/* Label styling */}
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
                  Phone
                </p>
                {/* User phone */}
                <p className="text-gray-900">{mockUser.phone}</p>
              </div>
            </div>
            {/* Suggestions Section - Updated with Aramex Red Theme */}
            <div className="mt-7 pt-5 border-t border-gray-200">
              {/* Section title */}
              <h4 className="font-bold text-gray-900 mb-4">
                Try asking:
              </h4>
              {/* Suggestion list with Aramex red bullets */}
              <ul className="text-gray-600 space-y-2.5">
                <li className="flex items-start">
                  {/* Bullet point in Aramex red */}
                  <span className="mr-2 text-red-600">•</span> {/* text-primary-600 -> text-red-600 */}
                  <span>Show me my recent shipments</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2 text-red-600">•</span>
                  <span>What's the status of package TN-ID?</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2 text-red-600">•</span>
                  <span>When will my package arrive?</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
        {/* Chat Interface - Ensure consistent styling */}
        <div className="lg:col-span-3">
          {/* Increased height for better chat experience on larger screens */}
          <div className="h-[500px] lg:h-[650px]">
            <ChatInterface userType="authenticated" userId={mockUser.id} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthenticatedChat;