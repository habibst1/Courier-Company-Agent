import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import AuthenticatedChat from './pages/AuthenticatedChat';
import AnonymousChat from './pages/AnonymousChat';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/authenticated" element={<AuthenticatedChat />} />
            <Route path="/anonymous" element={<AnonymousChat />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;