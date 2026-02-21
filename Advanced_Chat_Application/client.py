import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

HOST = "127.0.0.1"
PORT = 5050


# CONNECT
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.recv(1024)

root = tk.Tk()
root.withdraw()

choice = simpledialog.askstring("Authentication", "Type LOGIN or REGISTER").upper()

username = simpledialog.askstring("Username", "Enter Username:")
password = simpledialog.askstring("Password", "Enter Password:", show="*")

client.send(f"{choice}|{username}|{password}".encode())

response = client.recv(1024).decode()

if response == "REGISTER_SUCCESS":
    messagebox.showinfo("Success", "Registered Successfully. Login again.")
    exit()

if response == "REGISTER_FAIL":
    messagebox.showerror("Error", "Username already exists.")
    exit()

if response == "LOGIN_FAIL":
    messagebox.showerror("Error", "Invalid credentials.")
    exit()

if response == "DUPLICATE":
    messagebox.showerror("Error", "User already logged in.")
    exit()

# ROOM
room = simpledialog.askstring("Room", "Enter Chat Room Name:")
client.send(room.encode())

# GUI
root.deiconify()
root.title(f"Chat Room: {room}")
root.geometry("500x600")

chat_area = scrolledtext.ScrolledText(root)
chat_area.pack(padx=10, pady=10)
chat_area.config(state="disabled")

message_entry = tk.Entry(root, width=40)
message_entry.pack(side="left", padx=10, pady=10)


def send_message():
    msg = message_entry.get()
    if msg:
        client.send(msg.encode())
        message_entry.delete(0, tk.END)


tk.Button(root, text="Send", command=send_message).pack(side="left")


def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            chat_area.config(state="normal")
            chat_area.insert(tk.END, message + "\n")
            chat_area.config(state="disabled")
        except:
            break


threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()