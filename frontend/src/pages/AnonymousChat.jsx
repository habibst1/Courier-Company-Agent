import { useCallback, useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { startTracking } from '../api';
import ChatInterface from '../components/ChatInterface';
import TrackingForm from '../components/TrackingForm';
import { KEYS, clear, load, save } from '../storage';

// Sent automatically (and not shown) when a tracking chat starts.
const FIRST_QUESTION = 'Give updates about the tracking number';

export default function AnonymousChat() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [chat, setChat] = useState(() => load(KEYS.recipientChat)); // { sessionToken, trackingNumber }
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);

  const track = useCallback(async (number) => {
    setBusy(true);
    setError(null);
    try {
      const session = await startTracking(number);
      const next = { sessionToken: session.session_token, trackingNumber: session.tracking_number };
      save(KEYS.recipientChat, next);
      setChat({ ...next, fresh: true });
    } catch (failure) {
      setError(failure.message);
    } finally {
      setBusy(false);
    }
  }, []);

  // Links from the home page arrive as /anonymous?number=...
  const requested = searchParams.get('number');
  useEffect(() => {
    if (!requested) return undefined;
    const timer = setTimeout(() => {
      setSearchParams({}, { replace: true });
      if (chat?.trackingNumber !== requested.toUpperCase()) track(requested);
    }, 0);
    return () => clearTimeout(timer);
  }, [requested, chat, track, setSearchParams]);

  const trackAnother = () => {
    clear(KEYS.recipientChat);
    setChat(null);
    setError(null);
  };

  const expired = useCallback((message) => {
    clear(KEYS.recipientChat);
    setChat(null);
    setError(message);
  }, []);

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="mb-3 text-3xl font-bold text-gray-900">Anonymous Tracking</h1>
        <p className="text-gray-600">Track packages without logging in using a tracking number</p>
      </div>

      {!chat ? (
        <div className="rounded-xl border border-gray-200 bg-white p-8 text-center shadow-md md:p-10">
          <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-primary-50">
            <svg className="h-8 w-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"
              />
            </svg>
          </div>
          <h2 className="mb-5 text-2xl font-bold text-gray-900">Enter Tracking Number</h2>
          <p className="mb-7 text-gray-600">Provide your package tracking number to get started with tracking</p>
          <TrackingForm onTrack={track} busy={busy} error={error} initialValue={requested ?? ''} />
        </div>
      ) : (
        <div>
          <div className="mb-6 flex flex-col justify-between gap-4 rounded-xl border border-gray-200 bg-white p-4 shadow-sm sm:flex-row sm:items-center">
            <div>
              <h2 className="text-xl font-bold text-gray-900">Tracking: {chat.trackingNumber}</h2>
              <p className="text-gray-600">Anonymous tracking session</p>
            </div>
            <button
              type="button"
              onClick={trackAnother}
              className="rounded-lg px-4 py-2 text-sm font-medium text-primary-600 transition hover:bg-primary-50 hover:text-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              Change Tracking Number
            </button>
          </div>
          <div className="h-[500px] lg:h-[650px]">
            <ChatInterface
              key={chat.sessionToken}
              sessionToken={chat.sessionToken}
              title="Tracking Service"
              placeholder="Ask about this package…"
              autoQuestion={chat.fresh ? FIRST_QUESTION : undefined}
              resume={!chat.fresh}
              onExpired={expired}
            />
          </div>
        </div>
      )}
    </div>
  );
}
