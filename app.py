import tkinter as tk
from tkinter import messagebox
import random
import json
import os
from datetime import date

DATA_FILE = "data.json"

# ---------- Load / Save ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"streak": 0, "last_date": "", "history": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# ---------- Suggestion Logic ----------
def suggest_activity():
    try:
        screen_time = int(entry_time.get())
        energy_level = energy_var.get().lower()
    except:
        result_label.config(text="⚠️ Enter valid input!")
        return

    threshold = 60

    activities = [
        {"name": "Take a walk for 10 minutes", "type": "physical", "score": 9},
        {"name": "Stretch or exercise", "type": "physical", "score": 8},
        {"name": "Read a chapter", "type": "cognitive", "score": 8},
        {"name": "Listen to a podcast", "type": "passive", "score": 6},
        {"name": "Call a friend", "type": "social", "score": 9}
    ]

    if screen_time <= threshold:
        result_label.config(text="✅ You're within your limit!")
        return

    for activity in activities:
        if energy_level == "low" and activity["type"] == "physical":
            activity["score"] -= 2
        elif energy_level == "high" and activity["type"] == "physical":
            activity["score"] += 1

        activity["score"] += random.randint(0, 2)

    activities.sort(key=lambda x: x["score"], reverse=True)

    top_score = activities[0]["score"]
    top = [a for a in activities if a["score"] == top_score]
    chosen = random.choice(top)

    result = chosen["name"]
    result_label.config(text=f"💡 {result}")

    # Save history
    data["history"].append(result)
    save_data(data)

    return result


# ---------- Streak Logic ----------
def update_streak():
    today = str(date.today())

    if data["last_date"] == today:
        return

    if data["last_date"]:
        yesterday = date.fromisoformat(data["last_date"])
        if (date.today() - yesterday).days == 1:
            data["streak"] += 1
        else:
            data["streak"] = 1
    else:
        data["streak"] = 1

    data["last_date"] = today
    save_data(data)

    streak_label.config(text=f"🔥 Streak: {data['streak']} days")


# ---------- Timer ----------
def start_focus():
    try:
        minutes = int(entry_time.get())
    except:
        result_label.config(text="⚠️ Enter valid time!")
        return

    update_streak()
    countdown(minutes * 60)


def countdown(seconds):
    if seconds > 0:
        mins = seconds // 60
        secs = seconds % 60
        timer_label.config(text=f"{mins:02d}:{secs:02d}")
        root.after(1000, countdown, seconds - 1)
    else:
        timer_label.config(text="⏰ Time's up!")

        suggestion = suggest_activity()

        # Popup alert
        messagebox.showinfo("Break Time!", f"Try this instead:\n\n{suggestion}")


# ---------- UI ----------
root = tk.Tk()
root.title("Dopamine Focus App")
root.geometry("420x460")
root.configure(bg="#e8f0f2")

card = tk.Frame(root, bg="white")
card.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400)

tk.Label(card, text="🧠 Focus Mode",
         font=("Segoe UI", 16, "bold"),
         bg="white").pack(pady=10)

# Streak display
streak_label = tk.Label(card, text=f"🔥 Streak: {data['streak']} days",
                        bg="white", font=("Segoe UI", 10))
streak_label.pack()

tk.Label(card, text="Time (minutes)", bg="white").pack()
entry_time = tk.Entry(card, justify="center")
entry_time.pack(pady=5)

tk.Label(card, text="Energy Level", bg="white").pack()

energy_var = tk.StringVar(value="low")

frame_radio = tk.Frame(card, bg="white")
frame_radio.pack()

tk.Radiobutton(frame_radio, text="Low", variable=energy_var,
               value="low", bg="white").pack(side="left", padx=10)

tk.Radiobutton(frame_radio, text="High", variable=energy_var,
               value="high", bg="white").pack(side="left", padx=10)

tk.Button(card, text="💡 Get Suggestion",
          command=suggest_activity,
          bg="#4CAF50", fg="white", width=20).pack(pady=8)

tk.Button(card, text="⏱️ Start Focus",
          command=start_focus,
          bg="#2196F3", fg="white", width=20).pack(pady=5)

timer_label = tk.Label(card, text="",
                       font=("Segoe UI", 14, "bold"),
                       bg="white")
timer_label.pack(pady=10)

result_label = tk.Label(card, text="",
                        wraplength=250,
                        bg="white")
result_label.pack(pady=10)

root.mainloop()