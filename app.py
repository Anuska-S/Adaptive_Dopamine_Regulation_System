import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import date
import threading
import time
import random

# ---------- DATA FILE ----------
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"streak": 0, "last_date": ""}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ---------- STREAK ----------
def update_streak():
    data = load_data()
    today = str(date.today())

    if data["last_date"]:
        last = date.fromisoformat(data["last_date"])
        if (date.today() - last).days == 1:
            data["streak"] += 1
        else:
            data["streak"] = 1
    else:
        data["streak"] = 1

    data["last_date"] = today
    save_data(data)

    days_text = "day" if data["streak"] == 1 else "days"
    streak_label.config(text=f"🔥 Streak: {data['streak']} {days_text}")

# ---------- SUGGESTION ----------
def get_suggestion():
    try:
        screen_time = int(screen_entry.get())
        energy = energy_var.get()

        if screen_time > 180:
            if energy == "Low":
                options = ["Take a nap 💤", "Relax your mind 🌿", "Listen to calm music 🎧"]
            else:
                options = ["Workout 💪", "Go for a walk 🚶", "Stretch 🧘"]

        elif screen_time > 90:
            options = ["Read a book 📖", "Listen to podcast 🎧", "Write something ✍️"]

        else:
            options = ["Stay focused 🔥", "You're doing great 💯", "Keep going 👏"]

        suggestion = random.choice(options)
        suggestion_label.config(text=f"💡 {suggestion}")

        update_streak()

    except:
        suggestion_label.config(text="⚠️ Enter valid number")

# ---------- TIMER ----------
def start_timer():
    try:
        minutes = int(timer_entry.get())
        seconds = minutes * 60

        def countdown():
            nonlocal seconds
            while seconds > 0:
                mins, secs = divmod(seconds, 60)
                timer_label.config(text=f"⏳ {mins:02}:{secs:02}")
                time.sleep(1)
                seconds -= 1

            timer_label.config(text="⏰ Time's up!")
            messagebox.showinfo("Break Time!", "Take a break 😊")

        threading.Thread(target=countdown, daemon=True).start()

    except:
        timer_label.config(text="⚠️ Enter valid time")

# ---------- UI ----------
root = tk.Tk()
root.title("FocusFlow - Dopamine Regulation")
root.geometry("420x450")
root.configure(bg="#1e1e1e")

# Title
tk.Label(root, text="🧠 FocusFlow", font=("Arial", 16, "bold"),
         bg="#1e1e1e", fg="white").pack(pady=10)

# Screen input
tk.Label(root, text="Screen Time (minutes)", bg="#1e1e1e", fg="white").pack()
screen_entry = tk.Entry(root)
screen_entry.pack(pady=5)

# Energy
tk.Label(root, text="Energy Level", bg="#1e1e1e", fg="white").pack()

energy_var = tk.StringVar(value="Low")

tk.Radiobutton(root, text="Low", variable=energy_var, value="Low",
               bg="#1e1e1e", fg="white", selectcolor="#333").pack()
tk.Radiobutton(root, text="High", variable=energy_var, value="High",
               bg="#1e1e1e", fg="white", selectcolor="#333").pack()

# Button
tk.Button(root, text="Get Suggestion", command=get_suggestion,
          bg="#333", fg="white").pack(pady=10)

# Suggestion output
suggestion_label = tk.Label(root, text="", bg="#1e1e1e", fg="white")
suggestion_label.pack()

# Streak
streak_label = tk.Label(root, text="🔥 Streak: 0 days",
                        bg="#1e1e1e", fg="white")
streak_label.pack(pady=10)

# Timer
tk.Label(root, text="Focus Timer (minutes)",
         bg="#1e1e1e", fg="white").pack()

timer_entry = tk.Entry(root)
timer_entry.pack()

timer_label = tk.Label(root, text="⏳ Timer",
                       bg="#1e1e1e", fg="white")
timer_label.pack(pady=5)

tk.Button(root, text="Start Timer", command=start_timer,
          bg="#444", fg="white").pack()

root.mainloop()