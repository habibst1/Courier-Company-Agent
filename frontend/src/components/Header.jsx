import { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';

const links = [
  { to: '/', label: 'Home', end: true },
  { to: '/authenticated', label: 'Customer Service' },
  { to: '/anonymous', label: 'Anonymous Tracking' },
];

const linkClass = ({ isActive }) =>
  `block rounded-md px-4 py-2 text-sm font-medium transition ${
    isActive
      ? 'border border-primary-200 bg-primary-50 text-primary-700'
      : 'text-gray-600 hover:bg-gray-50 hover:text-primary-600'
  }`;

export default function Header() {
  const [open, setOpen] = useState(false);

  return (
    <header className="border-b border-gray-200 bg-white shadow-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <Link to="/" className="flex items-center gap-4" onClick={() => setOpen(false)}>
            <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary-600 text-xl font-bold text-white">
              C
            </span>
            <span className="text-2xl font-bold text-gray-900">CourierTrack AI</span>
          </Link>

          <nav className="hidden md:block" aria-label="Main">
            <div className="flex items-center space-x-1">
              {links.map((link) => (
                <NavLink key={link.to} to={link.to} end={link.end} className={linkClass}>
                  {link.label}
                </NavLink>
              ))}
            </div>
          </nav>

          <button
            type="button"
            className="rounded-md p-2 text-gray-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 md:hidden"
            aria-expanded={open}
            aria-controls="mobile-menu"
            aria-label={open ? 'Close menu' : 'Open menu'}
            onClick={() => setOpen((value) => !value)}
          >
            <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d={open ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16M4 18h16'}
              />
            </svg>
          </button>
        </div>

        {open && (
          <nav id="mobile-menu" className="space-y-1 pb-4 md:hidden" aria-label="Main">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                end={link.end}
                className={linkClass}
                onClick={() => setOpen(false)}
              >
                {link.label}
              </NavLink>
            ))}
          </nav>
        )}
      </div>
    </header>
  );
}
