import tkinter as tk
from tkinter import messagebox
import string
import secrets
import pyperclip

# Function to evaluate strength

def check_strength(password):
    score = 0

    if any(char.islower() for char in password):
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char in string.punctuation for char in password):
        score += 1
    if len(password) >= 12:
        score += 1

    if score <= 2:
        return "Weak", "red"
    elif score == 3 or score == 4:
        return "Medium", "orange"
    else:
        return "Strong", "green"

# Generate Password Function

def generate_password():
    try:
        length = int(length_entry.get())

        if length < 4:
            messagebox.showerror("Error", "Password length must be at least 4.")
            return

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
        return

    character_pool = ""

    if lower_var.get():
        character_pool += string.ascii_lowercase
    if upper_var.get():
        character_pool += string.ascii_uppercase
    if digit_var.get():
        character_pool += string.digits
    if symbol_var.get():
        character_pool += string.punctuation

    if not character_pool:
        messagebox.showerror("Error", "Select at least one character type.")
        return

    # Exclude confusing characters
    confusing_chars = "0O1lI"
    character_pool = ''.join(c for c in character_pool if c not in confusing_chars)

    password = ''.join(secrets.choice(character_pool) for _ in range(length))

    result_entry.delete(0, tk.END)
    result_entry.insert(0, password)

    strength, color = check_strength(password)
    strength_label.config(text=f"Strength: {strength}", fg=color)


# Copy to Clipboard

def copy_password():
    password = result_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# GUI Setup

root = tk.Tk()
root.title("Secure Password Generator")
root.geometry("450x500")
root.resizable(False, False)

# Title
title_label = tk.Label(root, text="🔐 Secure Password Generator", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Length
length_label = tk.Label(root, text="Password Length:")
length_label.pack()

length_entry = tk.Entry(root, width=10, justify="center")
length_entry.pack(pady=5)
length_entry.insert(0, "12")

# Character Options
lower_var = tk.BooleanVar(value=True)
upper_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Lowercase (a-z)", variable=lower_var).pack(anchor="w", padx=80)
tk.Checkbutton(root, text="Include Uppercase (A-Z)", variable=upper_var).pack(anchor="w", padx=80)
tk.Checkbutton(root, text="Include Numbers (0-9)", variable=digit_var).pack(anchor="w", padx=80)
tk.Checkbutton(root, text="Include Symbols (!@#)", variable=symbol_var).pack(anchor="w", padx=80)

# Generate Button
generate_btn = tk.Button(root, text="Generate Password", command=generate_password, bg="#4CAF50", fg="white")
generate_btn.pack(pady=15)

# Result
result_entry = tk.Entry(root, width=35, justify="center", font=("Arial", 12))
result_entry.pack(pady=10)

# Strength Label
strength_label = tk.Label(root, text="Strength: ", font=("Arial", 12, "bold"))
strength_label.pack()

# Copy Button
copy_btn = tk.Button(root, text="Copy to Clipboard", command=copy_password, bg="#2196F3", fg="white")
copy_btn.pack(pady=10)

root.mainloop()