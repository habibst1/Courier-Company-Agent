import { useCallback, useEffect, useRef, useState } from 'react';
import { ApiError, fetchHistory, streamReply } from '../api';

let counter = 0;
const newId = () => `m${(counter += 1)}`;

// Chat state for one session: the messages, a status line while the agent works,
// and whether a reply is in progress. One request runs at a time.
export function useChat(sessionToken, { onExpired } = {}) {
  const [messages, setMessages] = useState([]);
  const [status, setStatus] = useState(null);
  const [busy, setBusy] = useState(false);
  const [summarized, setSummarized] = useState(false);
  const busyRef = useRef(false);
  const controllerRef = useRef(null);

  // Cancel a request still in flight when the chat goes away.
  useEffect(() => () => controllerRef.current?.abort(), []);

  const begin = useCallback(() => {
    busyRef.current = true;
    setBusy(true);
    const controller = new AbortController();
    controllerRef.current = controller;
    return controller;
  }, []);

  const finish = useCallback(() => {
    busyRef.current = false;
    setBusy(false);
    setStatus(null);
  }, []);

  const showError = useCallback(
    (error) => {
      if (error.name === 'AbortError') return;
      if (error instanceof ApiError && error.status === 401) {
        onExpired?.(error.message);
        return;
      }
      setMessages((previous) => [...previous, { id: newId(), role: 'error', content: error.message }]);
    },
    [onExpired],
  );

  const loadHistory = useCallback(async () => {
    if (busyRef.current) return;
    const controller = begin();
    setStatus('Loading your conversation…');
    try {
      const history = await fetchHistory(sessionToken, controller.signal);
      setMessages(history.messages.map((message) => ({ id: newId(), ...message })));
      setSummarized(history.summarized);
    } catch (error) {
      showError(error);
    } finally {
      finish();
    }
  }, [sessionToken, showError, begin, finish]);

  const send = useCallback(
    async (text, { hidden = false } = {}) => {
      const message = text.trim();
      if (!message || busyRef.current) return;
      const controller = begin();
      setStatus(null);
      if (!hidden) setMessages((previous) => [...previous, { id: newId(), role: 'user', content: message }]);

      const replyId = newId();
      const showReply = (content, streaming) =>
        setMessages((previous) => {
          const reply = { id: replyId, role: 'assistant', content, streaming };
          const exists = previous.some((item) => item.id === replyId);
          return exists ? previous.map((item) => (item.id === replyId ? reply : item)) : [...previous, reply];
        });

      try {
        const reply = await streamReply({
          sessionToken,
          message,
          hidden,
          signal: controller.signal,
          onStatus: setStatus,
          onToken: (partial) => {
            setStatus(null);
            showReply(partial, true);
          },
        });
        showReply(reply, false);
      } catch (error) {
        setMessages((previous) => previous.filter((item) => item.id !== replyId));
        showError(error);
      } finally {
        finish();
      }
    },
    [sessionToken, showError, begin, finish],
  );

  return { messages, status, busy, summarized, send, loadHistory };
}
