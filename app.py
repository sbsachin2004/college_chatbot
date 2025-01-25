from flask import Flask, render_template, request, redirect, flash, jsonify
import csv

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Paths to CSV files
STAFF_FILE = "data/staff.csv"
TIMETABLE_FILE = "data/timetable.csv"

# Load data from CSV
def load_csv(filepath):
    data = []
    with open(filepath, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Save data to CSV
def save_csv(filepath, data):
    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["staff_name", "period", "class", "subject"])
        for row in data:
            writer.writerow([row["staff_name"], row["period"], row["class"], row["subject"]])

# Home route
@app.route("/")
def home():
    return render_template("login.html")

# Staff page
@app.route("/staff", methods=["GET", "POST"])
def staff():
    staff_data = load_csv(STAFF_FILE)
    staff_names = set([entry["staff_name"] for entry in staff_data])

    if request.method == "POST":
        staff_name = request.form["staff_name"]
        period = request.form["period"]
        
        timetable = load_csv(TIMETABLE_FILE)
        # Filter timetable data for the staff member
        staff_timetable = [entry for entry in timetable if entry["staff_name"] == staff_name]
        # Find period info for the selected period
        period_info = next((entry for entry in staff_timetable if entry["period"] == period), None)
        
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
        
        timetable = load_csv(TIMETABLE_FILE)
        # Filter timetable data by class
        class_timetable = {}
        
        for entry in timetable:
            if entry["class"] == class_name:
                # Add staff name to each timetable entry
                class_timetable[entry["period"]] = {
                    "subject": entry["subject"],
                    "staff_name": entry["staff_name"]
                }
        
        if class_timetable:
            return render_template("student_timetable.html", class_name=class_name, class_timetable=class_timetable)
        else:
            flash("No timetable found for the selected class.", "warning")

    return render_template("student.html")

if __name__ == "__main__":
    app.run(debug=True)
