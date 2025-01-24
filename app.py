from flask import Flask, render_template, request, redirect, flash, jsonify
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Paths to JSON files
STAFF_FILE = "data/staff.json"
TIMETABLE_FILE = "data/timetable.json"

# Load data from JSON
def load_json(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

# Save data to JSON
def save_json(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

# Home route
@app.route("/")
def home():
    return render_template("login.html")

# Staff page
@app.route("/staff", methods=["GET", "POST"])
def staff():
    staff_names = load_json(STAFF_FILE).keys()
    if request.method == "POST":
        staff_name = request.form["staff_name"]
        period = request.form["period"]
        
        timetable = load_json(TIMETABLE_FILE)
        staff_timetable = timetable.get(staff_name, {})
        period_info = staff_timetable.get(period, None)
        
        if period_info:
            return render_template("staff_timetable.html", staff_name=staff_name, period=period, period_info=period_info)
        else:
            flash("No information available for the selected period.", "warning")

    return render_template("staff.html", staff_names=staff_names)

# Student page
@app.route("/student", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        year = request.form["year"]
        department = request.form["department"]
        class_name = f"{department}-{year}"
        
        timetable = load_json(TIMETABLE_FILE)
        class_timetable = {period: details for staff, periods in timetable.items() for period, details in periods.items() if details["class"] == class_name}
        
        if class_timetable:
            return render_template("student_timetable.html", class_name=class_name, class_timetable=class_timetable)
        else:
            flash("No timetable found for the selected class.", "warning")

    return render_template("student.html")

if __name__ == "__main__":
    app.run(debug=True)
