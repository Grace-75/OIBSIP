import socket
import threading
import sqlite3
import hashlib
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5050

clients = {}
active_users = set()

# DATABASE SETUP
conn = sqlite3.connect("chat_database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    room TEXT,
    message TEXT,
    timestamp TEXT
)
""")
conn.commit()


# PASSWORD HASH
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# BROADCAST
def broadcast(room, message):
    for client, data in clients.items():
        if data["room"] == room:
            try:
                client.send(message.encode())
            except:
                remove_client(client)


# REMOVE CLIENT
def remove_client(client):
    if client in clients:
        username = clients[client]["username"]
        active_users.remove(username)
        del clients[client]
        client.close()


# HANDLE CLIENT
def handle_client(client):
    try:
        client.send("AUTH".encode())
        data = client.recv(1024).decode()
        action, username, password = data.split("|")

        if action == "REGISTER":
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                             (username, hash_password(password)))
                conn.commit()
                client.send("REGISTER_SUCCESS".encode())
            except:
                client.send("REGISTER_FAIL".encode())
            client.close()
            return

        if action == "LOGIN":
            cursor.execute("SELECT password FROM users WHERE username=?", (username,))
            result = cursor.fetchone()

            if not result or result[0] != hash_password(password):
                client.send("LOGIN_FAIL".encode())
                client.close()
                return

            if username in active_users:
                client.send("DUPLICATE".encode())
                client.close()
                return

            active_users.add(username)
            client.send("LOGIN_SUCCESS".encode())

        # Room selection
        room = client.recv(1024).decode()
        clients[client] = {"username": username, "room": room}

        # Send previous messages
        cursor.execute("SELECT username, message, timestamp FROM messages WHERE room=?", (room,))
        history = cursor.fetchall()

        for user, msg, time in history:
            client.send(f"[{time}] {user}: {msg}".encode())

        while True:
            message = client.recv(1024).decode()
            timestamp = datetime.now().strftime("%H:%M")

            formatted = f"[{timestamp}] {username}: {message}"

            cursor.execute("INSERT INTO messages (username, room, message, timestamp) VALUES (?, ?, ?, ?)",
                           (username, room, message, timestamp))
            conn.commit()

            broadcast(room, formatted)

    except:
        remove_client(client)


# START SERVER
def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("Server running on 127.0.0.1:5050")

    while True:
        client, _ = server.accept()
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    start()