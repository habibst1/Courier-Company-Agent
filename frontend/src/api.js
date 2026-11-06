// Every call to the backend goes through this file.
const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '');

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

async function errorMessage(response) {
  try {
    const body = await response.json();
    if (typeof body.detail === 'string') return body.detail;
    if (Array.isArray(body.detail) && body.detail[0]?.msg) return 'Please check what you typed and try again.';
  } catch {
    // Not a JSON error body.
  }
  return `The server answered with an error (${response.status}). Please try again.`;
}

async function request(path, { method = 'GET', token, body, signal } = {}) {
  const headers = {};
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  if (token) headers.Authorization = `Bearer ${token}`;
  let response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      method,
      headers,
      signal,
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  } catch (error) {
    if (error.name === 'AbortError') throw error;
    throw new ApiError("Can't reach the CourierTrack server. Check that the backend is running.", 0);
  }
  if (!response.ok) throw new ApiError(await errorMessage(response), response.status);
  return response;
}

export async function signIn(username, password) {
  const response = await request('/api/auth/login', { method: 'POST', body: { username, password } });
  return response.json(); // { access_token, user }
}

export async function startCustomerChat(accessToken) {
  const response = await request('/api/sessions', {
    method: 'POST',
    token: accessToken,
    body: { mode: 'customer' },
  });
  return response.json(); // { session_token, customer }
}

export async function startTracking(trackingNumber) {
  const response = await request('/api/sessions', {
    method: 'POST',
    body: { mode: 'recipient', tracking_number: trackingNumber },
  });
  return response.json(); // { session_token, tracking_number }
}

export async function fetchHistory(sessionToken, signal) {
  const response = await request('/api/chat/history', { token: sessionToken, signal });
  return response.json(); // { messages: [{ role, content }], summarized }
}

function parseEvent(block) {
  let type = 'message';
  const data = [];
  for (const line of block.split(/\r?\n/)) {
    if (line.startsWith('event:')) type = line.slice(6).trim();
    else if (line.startsWith('data:')) data.push(line.slice(5).trimStart());
  }
  if (data.length === 0) return null;
  try {
    return { type, data: JSON.parse(data.join('\n')) };
  } catch {
    return null;
  }
}

// Sends a message and streams the reply. onToken receives the reply text written so far.
export async function streamReply({ sessionToken, message, hidden = false, signal, onStatus, onToken }) {
  const response = await request('/api/chat/stream', {
    method: 'POST',
    token: sessionToken,
    body: { message, hidden },
    signal,
  });
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let partial = '';
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    let boundary = buffer.search(/\r?\n\r?\n/);
    while (boundary !== -1) {
      const separator = buffer.slice(boundary).match(/^\r?\n\r?\n/)[0];
      const event = parseEvent(buffer.slice(0, boundary));
      buffer = buffer.slice(boundary + separator.length);
      if (event?.type === 'status') onStatus?.(event.data.text);
      if (event?.type === 'token') {
        partial += event.data.text;
        onToken?.(partial);
      }
      if (event?.type === 'done') return event.data.reply;
      if (event?.type === 'error') throw new ApiError(event.data.message, 503);
      boundary = buffer.search(/\r?\n\r?\n/);
    }
  }
  throw new ApiError('The reply was cut off. Please try again.', 0);
}
