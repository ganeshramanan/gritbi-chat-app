"""
Gritbi Project #4: Real-time Chat Application
A Flask + Flask-SocketIO app for multi-room real-time messaging with live presence.

Teaching goals for students:
- WebSocket-based real-time communication (vs traditional request/response)
- Room-based message broadcasting
- In-memory state management (active users per room)
- Event-driven architecture (connect, disconnect, message, typing events)
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "gritbi-chat-secret"
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory state: { room_name: set(usernames) }
active_rooms = {}


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("join")
def handle_join(data):
    username = data.get("username", "Anonymous").strip() or "Anonymous"
    room = data.get("room", "general").strip() or "general"

    join_room(room)

    if room not in active_rooms:
        active_rooms[room] = set()
    active_rooms[room].add(username)

    emit("system_message", {
        "text": f"{username} joined the room",
        "time": datetime.now().strftime("%H:%M")
    }, room=room)

    emit("user_list", {"users": list(active_rooms[room])}, room=room)


@socketio.on("leave")
def handle_leave(data):
    username = data.get("username", "Anonymous")
    room = data.get("room", "general")

    leave_room(room)

    if room in active_rooms and username in active_rooms[room]:
        active_rooms[room].discard(username)

    emit("system_message", {
        "text": f"{username} left the room",
        "time": datetime.now().strftime("%H:%M")
    }, room=room)

    emit("user_list", {"users": list(active_rooms.get(room, []))}, room=room)


@socketio.on("send_message")
def handle_message(data):
    room = data.get("room", "general")
    username = data.get("username", "Anonymous")
    message = data.get("message", "").strip()

    if message:
        emit("receive_message", {
            "username": username,
            "message": message,
            "time": datetime.now().strftime("%H:%M")
        }, room=room)


@socketio.on("typing")
def handle_typing(data):
    room = data.get("room", "general")
    username = data.get("username", "Anonymous")
    emit("user_typing", {"username": username}, room=room, include_self=False)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5003, debug=True)
