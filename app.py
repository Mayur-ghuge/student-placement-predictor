from flask import Flask, render_template, request
import joblib
import numpy as np

from utils.db import get_db_connection

app = Flask(__name__)

# Load ML Model
model = joblib.load("model/placement_model.pkl")


# Home Page
@app.route("/")
def home():
    return render_template("home.html")


# Predict Page
@app.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "POST":

        # Form Data
        student_name = request.form["student_name"]
        department = request.form["department"]

        cgpa = float(request.form["cgpa"])
        aptitude = int(request.form["aptitude"])
        communication = int(request.form["communication"])
        coding = int(request.form["coding"])
        projects = int(request.form["projects"])
        internships = int(request.form["internships"])
        backlogs = int(request.form["backlogs"])

        # Prepare Features
        features = np.array([[
            cgpa,
            aptitude,
            communication,
            coding,
            projects,
            internships,
            backlogs
        ]])

        # Prediction
        prediction = model.predict(features)[0]

        # Placement Probability
        probabilities = model.predict_proba(features)[0]

        probability = round(
            probabilities[1] * 100,
            2
        )

        result = (
            "Likely To Be Placed"
            if prediction == 1
            else "Not Likely To Be Placed"
        )

        # Save to MySQL
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO predictions (
            student_name,
            department,
            cgpa,
            aptitude_score,
            communication_score,
            coding_score,
            projects,
            internships,
            backlogs,
            probability,
            prediction_result
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            student_name,
            department,
            cgpa,
            aptitude,
            communication,
            coding,
            projects,
            internships,
            backlogs,
            probability,
            result
        )

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()

        return render_template(
            "result.html",
            result=result,
            probability=probability
        )

    return render_template("predict.html")


# Analytics Page
@app.route("/analytics")
def analytics():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM predictions")
    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS placed
        FROM predictions
        WHERE prediction_result='Likely To Be Placed'
    """)
    placed = cursor.fetchone()["placed"]

    cursor.execute("""
        SELECT COUNT(*) AS not_placed
        FROM predictions
        WHERE prediction_result='Not Likely To Be Placed'
    """)
    not_placed = cursor.fetchone()["not_placed"]

    cursor.execute("""
        SELECT AVG(probability) AS avg_probability
        FROM predictions
    """)
    avg_probability = cursor.fetchone()["avg_probability"]

    cursor.close()
    conn.close()

    return render_template(
        "analytics.html",
        total=total,
        placed=placed,
        not_placed=not_placed,
        avg_probability=round(avg_probability or 0, 2)
    )


# History Page
@app.route("/history")
def history():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY id ASC
    """)

    predictions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "history.html",
        predictions=predictions
    )


# About Page
@app.route("/about")
def about():
    return render_template("about.html")


# Test Database Connection
@app.route("/test-db")
def test_db():

    conn = get_db_connection()

    if conn.is_connected():
        conn.close()
        return "Database Connected Successfully!"

    return "Connection Failed"


if __name__ == "__main__":
    app.run(debug=True)