from flask import Flask, render_template, request
import sqlite3
import math

app = Flask(__name__)

# ---------------------------
# AI-LIKE DIET RECOMMENDER
# ---------------------------
def get_ai_diet(bmi, goal):
    if goal == "weight_loss":
        if bmi > 25:
            return [
                "High-protein meals (dal, eggs, tofu)",
                "Low-carb rotis",
                "Leafy salads",
                "Green tea",
                "Avoid fried/sugary foods",
            ]
        else:
            return [
                "Balanced Indian meals",
                "2–3 fruits daily",
                "Light exercise & walking",
            ]

    if goal == "weight_gain":
        return [
            "Calorie-dense foods (peanut butter, bananas, paneer)",
            "Milk with oats",
            "Strength training",
            "Eggs / legumes daily",
        ]

    if goal == "maintain":
        return [
            "Balanced protein + carbs",
            "Regular walking",
            "Plenty of water",
            "Seasonal fruits",
        ]

    return ["Eat balanced food throughout the day."]


# ---------------------------
# ROUTES
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        height = float(request.form["height"]) / 100
        weight = float(request.form["weight"])
        goal = request.form["goal"]

        bmi = weight / (height * height)
        calories = math.floor(24 * weight * 1.3)
        diet_type = goal.replace("_", " ").title()
        diet_list = get_ai_diet(bmi, goal)

        result = {
            "bmi": round(bmi, 2),
            "calories": calories,
            "diet": diet_type,
            "diet_list": diet_list
        }

        # -------------------------
        # SAVE HISTORY TO DATABASE
        # -------------------------
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bmi REAL,
                calories INTEGER,
                diet TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("INSERT INTO history (bmi, calories, diet) VALUES (?, ?, ?)",
                  (result["bmi"], calories, diet_type))
        conn.commit()
        conn.close()

    # -------------------------
    # FETCH LAST 5 ENTRIES
    # -------------------------
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT bmi, calories, diet, timestamp FROM history ORDER BY id DESC LIMIT 5")
    history = c.fetchall()
    conn.close()

    return render_template("index.html", result=result, history=history)


if __name__ == "__main__":
    app.run(debug=True)
