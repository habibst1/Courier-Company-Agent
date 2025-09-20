// src/components/MessageBubble.jsx
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const MessageBubble = ({ message, isUser }) => {
  const isBot = message.type === 'bot' || message.type === 'clarification' || message.type === 'error';
  const isError = message.type === 'error';
  const isClarification = message.type === 'clarification';

  // Custom components for better styling within the bubble - Updated with Aramex Red Theme where applicable
  const components = {
    p: ({ node, ...props }) => <p className="mb-2 last:mb-0" {...props} />,
    ul: ({ node, ...props }) => <ul className="list-disc list-inside mb-2 ml-2" {...props} />,
    ol: ({ node, ...props }) => <ol className="list-decimal list-inside mb-2 ml-2" {...props} />,
    li: ({ node, ...props }) => <li className="mb-1" {...props} />,
    strong: ({ node, ...props }) => <strong className="font-semibold" {...props} />,
    em: ({ node, ...props }) => <em className="italic" {...props} />,
    h1: ({ node, ...props }) => <h1 className="text-xl font-bold mb-3 mt-4" {...props} />,
    h2: ({ node, ...props }) => <h2 className="text-lg font-semibold mb-2 mt-3" {...props} />,
    h3: ({ node, ...props }) => <h3 className="font-semibold mb-2 mt-2" {...props} />,
    // Adjusted code and pre for better integration and horizontal scrolling
    code: ({ node, inline, ...props }) =>
      inline ? (
        <code className="bg-gray-200 px-1.5 py-0.5 rounded font-mono text-sm" {...props} />
      ) : (
        // Added scrollbar-hide for horizontal overflow if needed, though overflow-x-auto on parent usually handles it
        <code className="block bg-gray-100 p-3 rounded-lg my-2 text-sm font-mono overflow-x-auto scrollbar-hide" {...props} />
      ),
    pre: ({ node, ...props }) => <pre className="bg-gray-100 p-3 rounded-lg my-2 overflow-x-auto scrollbar-hide" {...props} />,
    blockquote: ({ node, ...props }) => <blockquote className="border-l-4 border-gray-300 pl-4 italic text-gray-600 my-2" {...props} />,
    // Key Fix: Ensure table inherits min-width and handles overflow
    table: ({ node, ...props }) => <table className="min-w-full border-collapse border border-gray-300 my-2 text-sm" {...props} />,
    thead: ({ node, ...props }) => <thead className="bg-gray-50" {...props} />,
    th: ({ node, ...props }) => <th className="border border-gray-300 px-3 py-2 text-left font-semibold" {...props} />,
    td: ({ node, ...props }) => <td className="border border-gray-300 px-3 py-2" {...props} />,
    tr: ({ node, ...props }) => <tr className="even:bg-gray-50" {...props} />,
    // Updated link styling to use Aramex Red Theme
    a: ({ node, ...props }) => <a className="text-red-600 underline hover:text-red-700" {...props} />, // text-primary-600 -> text-red-600, hover:text-primary-700 -> hover:text-red-700
  };

  const renderContent = () => {
    if (isClarification) {
      return `**Need clarification:** ${message.message}`;
    } else if (isError) {
      return `**Error:** ${message.message}`;
    } else {
      return message.content || message.response || message.message || '';
    }
  };

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      {/* Increased max-width for better readability on larger screens and adjusted padding */}
      {/* KEY FIX: Added overflow-hidden to the main bubble container and overflow-x-auto to the markdown wrapper */}
      <div
        className={`relative max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg xl:max-w-xl px-4 py-3 rounded-2xl overflow-hidden ${ // Added overflow-hidden here
          isUser
            // Updated user message background to Aramex Red
            ? 'bg-red-600 text-white rounded-br-none' // bg-primary-600 -> bg-red-600
            : isError
            ? 'bg-red-50 border border-red-200 text-red-800'
            : isClarification
            ? 'bg-yellow-50 border border-yellow-200 text-yellow-800'
            : 'bg-gray-50 border border-gray-200 text-gray-800 rounded-bl-none'
        }`}
      >
        {isUser ? (
          <div>{message.content || message.response || message.message}</div>
        ) : (
          // KEY FIX: Wrapped ReactMarkdown in a div with overflow-x-auto
          <div className="overflow-x-auto"> {/* This div handles horizontal scrolling for wide content like tables */}
            <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
              {renderContent()}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;