from flask import Flask, render_template, request

app = Flask(__name__)

def get_diet_recommendation(goal, bmi):
    if goal == "Lose Weight":
        return (
            "• High-protein diet (eggs, paneer, dal, tofu)\n"
            "• Low-carb meals (millets, oats, salads)\n"
            "• Avoid sugar & fried foods\n"
            "• Drink 3–4L water daily\n"
        )
    elif goal == "Gain Weight":
        return (
            "• High-calorie nutrient-dense foods\n"
            "• Peanut butter, bananas, dry fruits\n"
            "• Rice, roti, potatoes, paneer, chicken\n"
            "• 3 big meals + 2 snacks\n"
        )
    else:  # Maintain Weight
        return (
            "• Balanced diet with fruits, vegetables\n"
            "• Dal, rice, roti, lean protein\n"
            "• Healthy fats (nuts, seeds, ghee in moderation)\n"
            "• 2–3L water daily\n"
        )


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        height = float(request.form["height"]) / 100
        weight = float(request.form["weight"])
        goal = request.form["goal"]

        bmi = round(weight / (height ** 2), 2)

        # calorie logic
        if goal == "Lose Weight":
            calories = int(weight * 22 * 0.85)
        elif goal == "Gain Weight":
            calories = int(weight * 22 * 1.15)
        else:
            calories = int(weight * 22)

        diet = get_diet_recommendation(goal, bmi)

        result = {
            "bmi": bmi,
            "calories": calories,
            "diet": diet
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
