import { useState } from 'react';
import { signIn } from '../api';

export default function LoginForm({ onSignedIn, notice }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);

  const submit = async (event) => {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      onSignedIn(await signIn(username.trim(), password));
    } catch (failure) {
      setError(failure.message);
      setBusy(false);
    }
  };

  const inputClass =
    'mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary-500';

  return (
    <div className="mx-auto max-w-md rounded-xl border border-gray-200 bg-white p-8 shadow-md">
      <h2 className="text-2xl font-bold text-gray-900">Sign in</h2>
      <p className="mt-2 text-gray-600">Sign in to see your shipments and chat with your assistant.</p>
      {notice && (
        <p role="status" className="mt-4 rounded-lg bg-yellow-50 px-4 py-3 text-sm text-yellow-800">
          {notice}
        </p>
      )}
      <form onSubmit={submit} className="mt-6 space-y-4">
        <div>
          <label htmlFor="login-username" className="text-sm font-medium text-gray-700">
            User name or email
          </label>
          <input
            id="login-username"
            type="text"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            autoComplete="username"
            required
            className={inputClass}
          />
        </div>
        <div>
          <label htmlFor="login-password" className="text-sm font-medium text-gray-700">
            Password
          </label>
          <input
            id="login-password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
            required
            className={inputClass}
          />
        </div>
        {error && (
          <p role="alert" className="text-sm text-red-700">
            {error}
          </p>
        )}
        <button
          type="submit"
          disabled={busy}
          className="w-full rounded-lg bg-primary-600 px-6 py-3 font-semibold text-white transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:bg-gray-300"
        >
          {busy ? 'Signing in…' : 'Sign in'}
        </button>
      </form>
      <p className="mt-6 text-xs text-gray-500">
        Demo accounts use the user names from the sample data, such as{' '}
        <code className="rounded bg-gray-100 px-1">habib_bencheikhali</code>, with the DEMO_PASSWORD from{' '}
        <code className="rounded bg-gray-100 px-1">backend/.env</code>.
      </p>
    </div>
  );
}
