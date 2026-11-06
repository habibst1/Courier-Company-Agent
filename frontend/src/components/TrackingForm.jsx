import { useState } from 'react';

export default function TrackingForm({ onTrack, busy = false, error, initialValue = '' }) {
  const [value, setValue] = useState(initialValue);

  const submit = (event) => {
    event.preventDefault();
    const trackingNumber = value.trim();
    if (trackingNumber && !busy) onTrack(trackingNumber);
  };

  return (
    <form onSubmit={submit} className="mx-auto max-w-md">
      <label htmlFor="tracking-number" className="sr-only">
        Tracking number
      </label>
      <div className="flex">
        <input
          id="tracking-number"
          type="text"
          value={value}
          onChange={(event) => setValue(event.target.value)}
          placeholder="e.g. TN4255-8215-9617"
          autoComplete="off"
          spellCheck="false"
          aria-invalid={Boolean(error)}
          aria-describedby={error ? 'tracking-error' : undefined}
          className="min-w-0 flex-1 rounded-l-lg border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
        <button
          type="submit"
          disabled={busy || !value.trim()}
          className="rounded-r-lg bg-primary-600 px-6 py-3 font-medium text-white transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:bg-gray-300"
        >
          {busy ? 'Checking…' : 'Track'}
        </button>
      </div>
      {error && (
        <p id="tracking-error" role="alert" className="mt-3 text-sm text-red-700">
          {error}
        </p>
      )}
    </form>
  );
}
