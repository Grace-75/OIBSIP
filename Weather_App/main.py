"""
Task 1
Advanced Weather Application
Python Development Internship Project

"""

import tkinter as tk
from tkinter import messagebox, ttk
import requests
from dotenv import load_dotenv
import os
from PIL import Image, ImageTk
from io import BytesIO


# LOAD API KEY

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# FETCH WEATHER DATA

def fetch_weather(city, unit):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": unit
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code != 200:
            return None

        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].title(),
            "wind": data["wind"]["speed"],
            "icon": data["weather"][0]["icon"]
        }

    except requests.exceptions.RequestException:
        return None


# FETCH WEATHER ICON

def fetch_icon(icon_code):
    try:
        url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        return ImageTk.PhotoImage(image)
    except:
        return None


# CHANGE BACKGROUND

def change_background(condition):
    condition = condition.lower()

    if "clear" in condition:
        color = "#4da6ff"
    elif "cloud" in condition:
        color = "#708090"
    elif "rain" in condition:
        color = "#2f4f4f"
    elif "mist" in condition or "haze" in condition:
        color = "#a9a9a9"
    elif "snow" in condition:
        color = "#f0f8ff"
    else:
        color = "#1e3d59"

    text_color = "black" if color in ["#f0f8ff", "#a9a9a9", "#4da6ff"] else "white"

    app.configure(bg=color)
    title_label.configure(bg=color, fg=text_color)
    result_label.configure(bg=color, fg=text_color)
    icon_label.configure(bg=color)
    unit_frame.configure(bg=color)
    unit_label.configure(bg=color, fg=text_color)


# BUTTON FUNCTION

def get_weather():
    city = city_entry.get().strip()
    unit = unit_var.get()

    if not city:
        messagebox.showwarning("Warning", "Please enter a city name.")
        return

    result_label.config(text="Fetching weather...")
    icon_label.config(image="")
    app.update()

    weather = fetch_weather(city, unit)

    if weather is None:
        messagebox.showerror("Error", "City not found or API issue.")
        result_label.config(text="")
        return

    symbol = "°C" if unit == "metric" else "°F"

    output = (
        f"City: {weather['city']}\n\n"
        f"Temperature: {weather['temp']} {symbol}\n"
        f"Humidity: {weather['humidity']} %\n"
        f"Condition: {weather['description']}\n"
        f"Wind Speed: {weather['wind']} m/s"
    )

    result_label.config(text=output)

    icon = fetch_icon(weather["icon"])
    if icon:
        icon_label.config(image=icon)
        icon_label.image = icon

    change_background(weather["description"])


# GUI SETUP

app = tk.Tk()
app.title("Advanced Weather App")
app.geometry("480x500")
app.resizable(False, False)
app.configure(bg="#1e3d59")


# Title
title_label = tk.Label(
    app,
    text="Weather Application",
    font=("Helvetica", 22, "bold"),
    bg="#1e3d59",
    fg="white"
)
title_label.pack(pady=20)


# City Entry
city_entry = tk.Entry(
    app,
    width=30,
    font=("Arial", 12),
    justify="center"
)
city_entry.pack(pady=10)


# Unit Selection
style = ttk.Style()
style.theme_use("clam")

unit_var = tk.StringVar()

unit_frame = tk.Frame(app, bg="#1e3d59")
unit_frame.pack(pady=5)

unit_label = tk.Label(
    unit_frame,
    text="Select Unit:",
    bg="#1e3d59",
    fg="white"
)
unit_label.pack(side="left", padx=5)

unit_combo = ttk.Combobox(
    unit_frame,
    textvariable=unit_var,
    values=["metric", "imperial"],
    state="readonly",
    width=10
)
unit_combo.set("metric")
unit_combo.pack(side="left")


# Button
search_button = tk.Button(
    app,
    text="Get Weather",
    command=get_weather,
    font=("Arial", 11, "bold"),
    bg="#ff6e40",
    fg="white",
    width=18
)
search_button.pack(pady=15)


# Result Label
result_label = tk.Label(
    app,
    text="",
    font=("Arial", 12),
    bg="#1e3d59",
    fg="white",
    justify="left"
)
result_label.pack(pady=20)


# Icon Label
icon_label = tk.Label(app, bg="#1e3d59")
icon_label.pack()


app.mainloop()
