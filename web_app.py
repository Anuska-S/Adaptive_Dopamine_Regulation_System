from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# ---------- LOAD DATA ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "daily_points": 0,
            "goal": 50,
            "theme": "light",
            "color": "blue",
            "focus_timer": 25,
            "break_timer": 5
        }

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    defaults = {
        "theme": "light",
        "color": "blue",
        "focus_timer": 25,
        "break_timer": 5
    }

    for key in defaults:
        if key not in data:
            data[key] = defaults[key]

    return data


# ---------- SAVE DATA ----------
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# ---------- HOME ----------
@app.route("/", methods=["GET", "POST"])
def home():
    data = load_data()

    message = ""
    show = False
    activities = []

    if request.method == "POST":
        time = int(request.form.get("time", 0))
        energy = request.form.get("energy")

        if time <= 60:
            message = "Within limit 👍"
            data["daily_points"] += 10
        else:
            message = "Exceeded. Choose better."
            show = True

            if energy == "high":
                activities = [
                    ("Walk for 30 mins", 20),
                    ("Mini workout", 40),
                    ("Clean your room", 15)
                ]
            else:
                activities = [
                    ("Read a chapter", 20),
                    ("Call a friend", 30),
                    ("Listen to music", 10),
                    ("Write a page", 15)
                ]

        save_data(data)

    progress = int((data["daily_points"] / data["goal"]) * 100)

    return render_template(
        "index.html",
        message=message,
        show=show,
        activities=activities,
        points=data["daily_points"],
        progress=progress
    )


# ---------- ADD POINTS ----------
@app.route("/add_points", methods=["POST"])
def add_points():
    data = load_data()

    pts = int(request.form.get("points", 0))
    data["daily_points"] += pts

    save_data(data)

    return redirect("/")


# ---------- SETTINGS ----------
@app.route("/settings", methods=["GET", "POST"])
def settings():
    data = load_data()

    if request.method == "POST":
        data["theme"] = request.form.get("theme", "light")
        data["color"] = request.form.get("color", "blue")
        data["focus_timer"] = int(request.form.get("focus_timer", 25))
        data["break_timer"] = int(request.form.get("break_timer", 5))

        save_data(data)

    return render_template("settings.html", data=data)


# ---------- RESET ----------
@app.route("/reset")
def reset():
    data = {
        "daily_points": 0,
        "goal": 50,
        "theme": "light",
        "color": "blue",
        "focus_timer": 25,
        "break_timer": 5
    }
    save_data(data)
    return redirect("/")


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)