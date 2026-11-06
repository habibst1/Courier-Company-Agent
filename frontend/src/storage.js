// Tokens and the current chat live in sessionStorage: they survive a reload but not closing
// the tab. Storage can be unavailable (private windows, blocked site data), so every access
// is guarded and the app keeps working without it.

export const KEYS = {
  login: 'couriertrack.login',
  customerChat: 'couriertrack.customerChat',
  recipientChat: 'couriertrack.recipientChat',
};

export function load(key) {
  try {
    const raw = window.sessionStorage.getItem(key);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function save(key, value) {
  try {
    window.sessionStorage.setItem(key, JSON.stringify(value));
  } catch {
    // Storage unavailable: the chat still works, it just won't survive a reload.
  }
}

export function clear(key) {
  try {
    window.sessionStorage.removeItem(key);
  } catch {
    // Nothing to clear.
  }
}
