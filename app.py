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
    staff_data = load_json(STAFF_FILE)
    staff_names = staff_data.keys()

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

# Add/Edit Staff Details
@app.route("/add_edit_staff", methods=["GET", "POST"])
def add_edit_staff():
    staff_data = load_json(STAFF_FILE)
    if request.method == "POST":
        staff_name = request.form["staff_name"]
        department = request.form["department"]
        email = request.form["email"]
        phone = request.form["phone"]

        # Check if the staff exists to edit or add new staff
        if staff_name in staff_data:
            staff_data[staff_name] = {
                "department": department,
                "email": email,
                "phone": phone
            }
            flash(f"Updated details for {staff_name}", "success")
        else:
            staff_data[staff_name] = {
                "department": department,
                "email": email,
                "phone": phone
            }
            flash(f"Added new staff: {staff_name}", "success")

        save_json(STAFF_FILE, staff_data)
        return redirect("/staff")

    return render_template("add_edit_staff.html")

# Add/Edit Timetable for Staff
@app.route("/add_edit_timetable", methods=["GET", "POST"])
def add_edit_timetable():
    timetable = load_json(TIMETABLE_FILE)

    if request.method == "POST":
        staff_name = request.form["staff_name"]
        period = request.form["period"]
        subject = request.form["subject"]
        class_name = request.form["class_name"]

        if staff_name not in timetable:
            timetable[staff_name] = {}

        timetable[staff_name][period] = {
            "subject": subject,
            "class": class_name
        }

        save_json(TIMETABLE_FILE, timetable)
        flash(f"Added timetable for {staff_name} for {period}", "success")
        return redirect("/staff")

    staff_names = load_json(STAFF_FILE).keys()
    return render_template("add_edit_timetable.html", staff_names=staff_names)

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
