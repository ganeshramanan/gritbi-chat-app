# Real-time Chat Application — Gritbi Project #4 (Tier 2)

A multi-room, real-time chat application built with **Flask + Flask-SocketIO**. Live messaging, presence tracking, and typing indicators — no page refresh needed.

## Features
- Join any named room (rooms are created on the fly)
- Real-time message broadcasting to everyone in the room
- Live online user list per room
- "User is typing..." indicator
- System messages when users join/leave

## Tech Stack
- **Backend**: Python, Flask, Flask-SocketIO (WebSocket support)
- **Async worker**: eventlet (required for WebSockets in production)
- **Frontend**: HTML, CSS, Socket.IO client (vanilla JS, no framework)
- **Deployment**: Render (gunicorn with eventlet worker)

## Running locally

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5003` — open multiple browser tabs to simulate multiple users chatting.

## What students will learn
1. **WebSockets vs HTTP** — why real-time apps need persistent connections instead of repeated polling
2. **Event-driven programming** — handling `connect`, `join`, `send_message`, `typing`, `disconnect` events
3. **Room-based broadcasting** — using Socket.IO "rooms" to scope messages to specific groups
4. **In-memory state management** — tracking active users per room (and its limitations — see customization ideas)
5. **Production WebSocket deployment** — why you need an async worker (eventlet/gevent) instead of default gunicorn sync workers

## Suggested customizations (for uniqueness per student)
- Persist chat history to a database (currently messages are not stored — refreshing loses history)
- Add private 1-to-1 messaging alongside room chat
- Add emoji reactions or file/image sharing
- Add user authentication instead of free-text usernames
- Add message read receipts

## Viva prep — common questions to expect
- What's the difference between WebSockets and traditional HTTP requests?
- Why can't you use a normal gunicorn worker for this app? What does `eventlet` do?
- How does the server know which users are in which room?
- What happens to chat history if the server restarts? How would you fix that?
- How would this app behave if 100 users joined the same room at once?

---
Built as part of **Gritbi** — learn to build, understand, and defend real projects.
