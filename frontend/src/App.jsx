import { BrowserRouter, Link, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import AnonymousChat from './pages/AnonymousChat';
import AuthenticatedChat from './pages/AuthenticatedChat';
import HomePage from './pages/HomePage';

function NotFound() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-24 text-center">
      <h1 className="mb-4 text-3xl font-bold text-gray-900">Page not found</h1>
      <Link to="/" className="font-medium text-primary-600 hover:text-primary-700">
        Back to the home page
      </Link>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/authenticated" element={<AuthenticatedChat />} />
            <Route path="/anonymous" element={<AnonymousChat />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
