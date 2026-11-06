# CourierTrack frontend

React 19 + Vite + Tailwind CSS. It talks to the FastAPI backend in `../backend`.

```bash
npm install
npm run dev      # http://localhost:5173
npm run lint
npm run build
```

The backend URL defaults to `http://localhost:8000`. To change it, copy `.env.example` to
`.env.local` and set `VITE_API_URL`.

| Path | What it does |
| --- | --- |
| `src/api.js` | Every backend call, including the streaming reader for `/api/chat/stream` |
| `src/hooks/useChat.js` | Chat state: messages, streaming text, status line, history loading |
| `src/storage.js` | Keeps tokens and the current chat in `sessionStorage` so a reload resumes it |
| `src/pages/` | Home, Customer Service (sign-in required) and Anonymous Tracking |
