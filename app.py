from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect
from pymongo import MongoClient
import sqlite3
import re
from bson import ObjectId
from config import Config

# INITIALIZE APP + SECURITY
app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)


# SQLITE (User Authentication DB)
def get_auth_db():
    conn = sqlite3.connect("database/auth.db")
    conn.row_factory = sqlite3.Row
    return conn


# MONGODB ATLAS (Patients)
mongo_client = MongoClient(
    "mongodb+srv://officialsujan47_db_user:Sujan12345@cluster0.zrgctuz.mongodb.net/?retryWrites=true&w=majority"
)

mongo_db = mongo_client["stroke_prediction"]
patient_collection = mongo_db["patients"]


# HELPERS
def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def login_required(f):
    from functools import wraps

    @wraps(f)
    def secure_route(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect("/login")
        return f(*args, **kwargs)

    return secure_route


# BASIC ROUTE
@app.route("/")
def home():
    return redirect("/dashboard")


# REGISTER USER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        if not validate_email(email):
            flash("Invalid email format.", "danger")
            return redirect("/register")

        hashed_pw = bcrypt.generate_password_hash(password).decode()

        db = get_auth_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, hashed_pw),
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash("Email already registered.", "danger")
            return redirect("/register")

        flash("Registration successful! Please login.", "success")
        return redirect("/login")

    return render_template("register.html")


# LOGIN USER
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form["email"]
        password_input = request.form["password"]

        db = get_auth_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user["password"], password_input):
            session["user_id"] = user["id"]
            session["email"] = user["email"]
            flash("Logged in successfully.", "success")
            return redirect("/dashboard")

        flash("Incorrect email or password.", "danger")

    return render_template("login.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect("/login")


# DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
    total_patients = patient_collection.count_documents({})
    return render_template("dashboard.html", total=total_patients)

# CREATE PATIENT
@app.route("/patients/create", methods=["GET", "POST"])
@login_required
def create_patient():

    if request.method == "POST":
        patient = {
            "id": int(request.form["id"]),
            "age": int(request.form["age"]),
            "gender": request.form["gender"],
            "hypertension": request.form.get("hypertension") == "1",
            "heart_disease": request.form.get("heart_disease") == "1",
            "ever_married": request.form["ever_married"],
            "work_type": request.form["work_type"],
            "residence_type": request.form["residence_type"],
            "avg_glucose_level": float(request.form["avg_glucose_level"]),
            "bmi": float(request.form["bmi"]),
            "smoking_status": request.form["smoking_status"],
            "stroke": int(request.form["stroke"])
        }

        patient_collection.insert_one(patient)
        flash("Patient added successfully!", "success")
        return redirect("/patients")

    return render_template("patient_create.html")

# PATIENTS LIST (READ)
@app.route("/patients")
@login_required
def patients():
    patients_list = list(patient_collection.find())
    return render_template("patients_list.html", patients=patients_list)


# VIEW PATIENT DETAILS
@app.route("/patients/view/<string:id>")
@login_required
def view_patient(id):
    patient = patient_collection.find_one({"_id": ObjectId(id)})
    return render_template("patient_view.html", patient=patient)


# EDIT PATIENT
@app.route("/patients/edit/<string:id>", methods=["GET", "POST"])
@login_required
def edit_patient(id):
    patient = patient_collection.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        update = {
            "name": request.form["name"],
            "age": int(request.form["age"]),
            "gender": request.form["gender"],
            "hypertension": request.form.get("hypertension") == "1",
            "heart_disease": request.form.get("heart_disease") == "1",
            "ever_married": request.form["ever_married"],
            "work_type": request.form["work_type"],
            "residence_type": request.form["residence_type"],
            "avg_glucose_level": float(request.form["avg_glucose_level"]),
            "bmi": float(request.form["bmi"]),
            "smoking_status": request.form["smoking_status"],
            "stroke": int(request.form["stroke"])
        }

        patient_collection.update_one({"_id": ObjectId(id)}, {"$set": update})
        flash("Patient updated successfully!", "success")
        return redirect("/patients")

    return render_template("patient_edit.html", patient=patient)


# RUN APP
if __name__ == "__main__":
    app.run(debug=True)
