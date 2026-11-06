import { useCallback, useEffect, useState } from 'react';
import { startCustomerChat } from '../api';
import ChatInterface from '../components/ChatInterface';
import LoginForm from '../components/LoginForm';
import { KEYS, clear, load, save } from '../storage';

const SUGGESTIONS = [
  'Show me my recent shipments',
  'Which of my packages are still in transit?',
  'When will my latest package arrive?',
];

function ProfileCard({ customer, onNewChat, onSignOut }) {
  const name = customer?.full_name || customer?.username || '';
  return (
    <div className="sticky top-6 rounded-xl border border-gray-200 bg-white p-6 shadow-md">
      <div className="mb-5 flex items-center">
        <div className="flex h-14 w-14 flex-shrink-0 items-center justify-center rounded-full bg-primary-50">
          <span className="text-xl font-bold text-primary-600">{name.charAt(0) || '?'}</span>
        </div>
        <div className="ml-4 overflow-hidden">
          <h3 className="truncate font-bold text-gray-900">{name || 'Loading…'}</h3>
          {customer?.username && <p className="truncate text-sm text-gray-600">@{customer.username}</p>}
        </div>
      </div>
      <dl className="space-y-4">
        {[
          ['Email', customer?.email],
          ['Phone', customer?.phone],
        ].map(([label, value]) => (
          <div key={label}>
            <dt className="mb-1 text-xs font-semibold uppercase tracking-wider text-gray-500">{label}</dt>
            <dd className="truncate text-gray-900">{value || '—'}</dd>
          </div>
        ))}
      </dl>
      <div className="mt-7 flex flex-col gap-2 border-t border-gray-200 pt-5">
        <button
          type="button"
          onClick={onNewChat}
          className="rounded-lg border border-primary-600 px-4 py-2 text-sm font-medium text-primary-600 transition hover:bg-primary-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          New conversation
        </button>
        <button
          type="button"
          onClick={onSignOut}
          className="rounded-lg px-4 py-2 text-sm font-medium text-gray-600 transition hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          Sign out
        </button>
      </div>
    </div>
  );
}

export default function AuthenticatedChat() {
  const [login, setLogin] = useState(() => load(KEYS.login)); // { accessToken, user }
  const [chat, setChat] = useState(() => load(KEYS.customerChat)); // { sessionToken, customer }
  const [notice, setNotice] = useState(null);
  const [error, setError] = useState(null);
  const [attempt, setAttempt] = useState(0);

  const signOut = useCallback((message) => {
    clear(KEYS.login);
    clear(KEYS.customerChat);
    setChat(null);
    setLogin(null);
    setNotice(typeof message === 'string' ? message : null);
  }, []);

  // Once signed in, open a chat session (a new conversation thread) if there isn't one.
  useEffect(() => {
    if (!login || chat) return undefined;
    let ignore = false;
    setError(null);
    startCustomerChat(login.accessToken)
      .then((session) => {
        if (ignore) return;
        const next = { sessionToken: session.session_token, customer: session.customer };
        save(KEYS.customerChat, next);
        setChat({ ...next, fresh: true });
      })
      .catch((failure) => {
        if (ignore) return;
        if (failure.status === 401) signOut(failure.message);
        else setError(failure.message);
      });
    return () => {
      ignore = true;
    };
  }, [login, chat, attempt, signOut]);

  const signedIn = ({ access_token: accessToken, user }) => {
    const next = { accessToken, user };
    save(KEYS.login, next);
    setNotice(null);
    setLogin(next);
  };

  const newConversation = () => {
    clear(KEYS.customerChat);
    setChat(null);
  };

  const firstName = (chat?.customer?.full_name || login?.user?.full_name || '').split(' ')[0];

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="mb-3 text-3xl font-bold text-gray-900">Customer Service Chat</h1>
        <p className="text-gray-600">Chat with our AI assistant about your shipments, deliveries and account.</p>
      </div>

      {!login ? (
        <LoginForm onSignedIn={signedIn} notice={notice} />
      ) : (
        <div className="grid gap-6 lg:grid-cols-4">
          <div className="lg:col-span-1">
            <ProfileCard
              customer={chat?.customer ?? login.user}
              onNewChat={newConversation}
              onSignOut={() => signOut()}
            />
          </div>
          <div className="h-[500px] lg:col-span-3 lg:h-[650px]">
            {chat ? (
              <ChatInterface
                key={chat.sessionToken}
                sessionToken={chat.sessionToken}
                title="Customer Assistant"
                greeting={`Hello${firstName ? ` ${firstName}` : ''}! I'm your courier assistant. How can I help you today?`}
                resume={!chat.fresh}
                suggestions={SUGGESTIONS}
                onExpired={newConversation}
              />
            ) : (
              <div className="flex h-full flex-col items-center justify-center gap-4 rounded-xl border border-gray-200 bg-white p-6 text-center shadow-md">
                {error ? (
                  <>
                    <p role="alert" className="text-red-700">
                      {error}
                    </p>
                    <button
                      type="button"
                      onClick={() => setAttempt((value) => value + 1)}
                      className="rounded-lg bg-primary-600 px-5 py-2 font-medium text-white hover:bg-primary-700"
                    >
                      Try again
                    </button>
                  </>
                ) : (
                  <p className="text-gray-600">Opening your chat…</p>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
