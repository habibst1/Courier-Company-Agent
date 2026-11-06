import { useEffect, useRef, useState } from 'react';
import { useChat } from '../hooks/useChat';
import MessageBubble from './MessageBubble';

function TypingIndicator({ label }) {
  return (
    <div className="flex justify-start">
      <div className="flex items-center gap-3 rounded-lg border border-gray-200 bg-white px-4 py-3 shadow-sm">
        <div className="flex space-x-1.5" aria-hidden="true">
          <span className="h-2.5 w-2.5 animate-bounce-slow rounded-full bg-primary-600" />
          <span className="h-2.5 w-2.5 animate-bounce-slow rounded-full bg-primary-600 [animation-delay:0.2s]" />
          <span className="h-2.5 w-2.5 animate-bounce-slow rounded-full bg-primary-600 [animation-delay:0.4s]" />
        </div>
        <span className="text-sm text-gray-600">{label || 'Thinking…'}</span>
      </div>
    </div>
  );
}

// A chat bound to one session. `resume` reloads its history; otherwise `autoQuestion`
// (if given) is sent once, hidden, to open the conversation.
export default function ChatInterface({
  sessionToken,
  title,
  greeting,
  placeholder = 'Ask about your shipments…',
  autoQuestion,
  resume = false,
  suggestions = [],
  onExpired,
}) {
  const { messages, status, busy, summarized, send, loadHistory } = useChat(sessionToken, { onExpired });
  const [draft, setDraft] = useState('');
  const startedRef = useRef(false);
  const endRef = useRef(null);

  // Deferred so React's development double-mount schedules it once instead of sending twice.
  useEffect(() => {
    const timer = setTimeout(() => {
      if (startedRef.current) return;
      startedRef.current = true;
      if (resume) loadHistory();
      else if (autoQuestion) send(autoQuestion, { hidden: true });
    }, 0);
    return () => clearTimeout(timer);
  }, [resume, autoQuestion, loadHistory, send]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ block: 'end' });
  }, [messages, status]);

  const submit = (event) => {
    event.preventDefault();
    if (!draft.trim() || busy) return;
    send(draft);
    setDraft('');
  };

  const streaming = messages.some((message) => message.streaming);
  const empty = messages.length === 0 && !busy;

  return (
    <section
      className="flex h-full flex-col overflow-hidden rounded-xl border border-gray-200 bg-white shadow-md"
      aria-label={title}
    >
      <header className="flex items-center gap-3 border-b border-gray-200 bg-gray-50 px-5 py-3.5">
        <span className="h-3.5 w-3.5 flex-shrink-0 rounded-full bg-green-500" aria-hidden="true" />
        <h2 className="text-sm font-semibold text-gray-800">{title}</h2>
      </header>

      <div className="scrollbar-hide flex-1 space-y-4 overflow-y-auto p-4 md:p-5" aria-live="polite">
        {summarized && (
          <p className="text-center text-xs text-gray-500">Earlier messages in this chat were summarized.</p>
        )}
        {greeting && empty && <MessageBubble message={{ role: 'assistant', content: greeting }} />}
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {busy && !streaming && <TypingIndicator label={status} />}
        <div ref={endRef} />
      </div>

      {empty && suggestions.length > 0 && (
        <div className="flex flex-wrap gap-2 px-4 pb-1">
          {suggestions.map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              onClick={() => send(suggestion)}
              className="rounded-full border border-primary-200 bg-primary-50 px-3 py-1.5 text-sm text-primary-700 transition hover:bg-primary-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}

      <form onSubmit={submit} className="border-t border-gray-200 p-4">
        <div className="flex rounded-lg shadow-sm transition focus-within:shadow-md">
          <label htmlFor="chat-message" className="sr-only">
            Message
          </label>
          <input
            id="chat-message"
            type="text"
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            placeholder={placeholder}
            maxLength={1000}
            autoComplete="off"
            disabled={busy}
            className="min-w-0 flex-1 rounded-l-lg border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:bg-gray-50"
          />
          <button
            type="submit"
            disabled={busy || !draft.trim()}
            className="rounded-r-lg bg-primary-600 px-5 py-3 font-medium text-white transition hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:bg-gray-300"
          >
            Send
          </button>
        </div>
      </form>
    </section>
  );
}
