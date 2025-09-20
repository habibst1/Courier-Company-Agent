// src/components/ChatInterface.jsx
import React, { useState, useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import axios from 'axios';

const ChatInterface = ({ userType, userId, initialTrackingNumber, initialQuestion }) => {
  const [messages, setMessages] = useState(
    userType === 'authenticated' 
      ? [{
          id: 1,
          type: 'bot',
          content: "Hello! I'm your courier assistant. How can I help you today?"
        }]
      : [] // Empty array for anonymous users
  );
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const requestRef = useRef(null); // Ref to track the current request
  const hasProcessedInitialQuestion = useRef(false); // Ref to track if initial question was processed

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Automatically ask about the tracking when an initial question is provided
  useEffect(() => {
    if (initialQuestion && !hasProcessedInitialQuestion.current) {
      // Mark as processed to prevent duplicate execution
      hasProcessedInitialQuestion.current = true;
      
      // Cancel any pending request
      if (requestRef.current) {
        requestRef.current.cancel();
      }
      
      // Show typing indicator immediately and make the API call
      setIsLoading(true);
      
      // Use setTimeout to ensure the typing indicator is rendered first
      setTimeout(() => {
        handleAutoQuestion(initialQuestion);
      }, 200);
    }
    // Cleanup function to cancel any pending requests
    return () => {
      if (requestRef.current) {
        requestRef.current.cancel();
      }
    };
  }, [initialQuestion]);

  const handleAutoQuestion = async (question) => {
    // Create a cancel token for this request
    const cancelTokenSource = axios.CancelToken.source();
    requestRef.current = cancelTokenSource;
    try {
      const response = await axios.post('http://localhost:8000/query', {
        question: question,
        user_id: userType === 'authenticated' ? userId : undefined,
        tracking_number: userType === 'anonymous' ? initialTrackingNumber : undefined
      }, {
        cancelToken: cancelTokenSource.token
      });
      const botMessage = {
        id: Date.now() + 1,
        type: response.data.type,
        content: response.data.response,
        data: response.data.data,
        message: response.data.message
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      if (axios.isCancel(error)) {
        console.log('Request canceled:', error.message);
      } else {
        const errorMessage = {
          id: Date.now() + 1,
          type: 'error',
          message: 'Sorry, I encountered an error processing your request.'
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } finally {
      setIsLoading(false);
      requestRef.current = null;
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    // Create a cancel token for this request
    const cancelTokenSource = axios.CancelToken.source();
    requestRef.current = cancelTokenSource;
    try {
      const response = await axios.post('http://localhost:8000/query', {
        question: inputValue,
        user_id: userType === 'authenticated' ? userId : undefined,
        tracking_number: userType === 'anonymous' ? initialTrackingNumber : undefined
      }, {
        cancelToken: cancelTokenSource.token
      });
      const botMessage = {
        id: Date.now() + 1,
        type: response.data.type,
        content: response.data.response,
        data: response.data.data,
        message: response.data.message
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      if (axios.isCancel(error)) {
        console.log('Request canceled:', error.message);
      } else {
        const errorMessage = {
          id: Date.now() + 1,
          type: 'error',
          message: 'Sorry, I encountered an error processing your request.'
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } finally {
      setIsLoading(false);
      requestRef.current = null;
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
      {/* Chat Header - Updated with Aramex Red Theme */}
      <div className="px-5 py-3.5 border-b border-gray-200 bg-gray-50 rounded-t-xl">
        <div className="flex items-center">
          {/* Online Status Indicator - Kept green for standard online status */}
          <div className="w-3.5 h-3.5 bg-green-500 rounded-full mr-3 flex-shrink-0"></div>
          {/* Updated header text color for better contrast */}
          <span className="text-sm font-semibold text-gray-800">
            {userType === 'authenticated' ? `Customer Assistant` : 'Tracking Service'}
          </span>
        </div>
      </div>
      
      {/* Messages Container - Kept consistent styling */}
      <div className="flex-1 overflow-y-auto p-4 md:p-5 scrollbar-hide">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} isUser={message.type === 'user'} />
        ))}
        {/* Typing Indicator - Updated with Aramex Red Theme */}
        {isLoading && (
          <div className="flex justify-start mb-4">
            {/* Applied consistent message bubble styling to the typing indicator */}
            <div className="bg-white border border-gray-200 text-gray-800 px-4 py-3 rounded-lg shadow-sm">
              <div className="flex space-x-1.5">
                {/* Updated typing indicator dots to Aramex Red */}
                <div className="w-2.5 h-2.5 bg-red-600 rounded-full animate-bounce-slow"></div> {/* bg-gray-400 -> bg-red-600 */}
                <div className="w-2.5 h-2.5 bg-red-600 rounded-full animate-bounce-slow" style={{ animationDelay: '0.2s' }}></div> {/* bg-gray-400 -> bg-red-600 */}
                <div className="w-2.5 h-2.5 bg-red-600 rounded-full animate-bounce-slow" style={{ animationDelay: '0.4s' }}></div> {/* bg-gray-400 -> bg-red-600 */}
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input Area - Updated with Aramex Red Theme */}
      <div className="border-t border-gray-200 p-4">
        <div className="flex">
          {/* Input Group - Updated focus ring and button colors */}
          <div className="flex-1 flex shadow-sm rounded-lg transition duration-200 focus-within:shadow-md">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about your shipments..."
              // Changed focus:ring-primary-500 to focus:ring-red-500
              className="flex-1 px-4 py-3 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim()}
              // Changed bg-primary-600 to bg-red-600, hover:bg-primary-700 to hover:bg-red-700
              // Changed disabled:bg-gray-300 (optional - you could use red-300 if preferred)
              className="bg-red-600 hover:bg-red-700 disabled:bg-gray-300 text-white px-5 py-3 rounded-r-lg font-medium transition duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-0"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;