from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DATABASE_NAME = os.getenv("DATABASE_NAME", "students.db")
PORT = int(os.getenv("PORT", 8081))


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        semester = request.form["semester"]

        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO students
            (name, email, course, semester)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, course, semester)
        )

        conn.commit()
        conn.close()

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        total_students=total_students
    )


@app.route("/students")
def students():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students
    )


@app.route("/delete/<int:id>")
def delete_student(id):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/students")


@app.route("/about")
def about():

    return render_template("about.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)