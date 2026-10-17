import os
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort

ROOT = Path(__file__).resolve().parent


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.getenv("SECRET_KEY",
                                           "change-me-in-production"),
                      DATABASE=os.getenv("DATABASE_PATH",
                                         str(ROOT / "students.db")))
    if test_config:
        app.config.update(test_config)

    def db():
        path = app.config["DATABASE"]
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        conn.execute("""CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT NOT NULL UNIQUE,
            course TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        return conn

    @app.get("/")
    def index():
        with db() as conn:
            total = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
            courses = conn.execute(
                "SELECT course, COUNT(*) count FROM students GROUP BY course ORDER BY count DESC LIMIT 5").fetchall()
            recent = conn.execute(
                "SELECT * FROM students ORDER BY id DESC LIMIT 5").fetchall()
        return render_template(
            "index.html",
            total=total,
            courses=courses,
            recent=recent)

    @app.get("/students")
    def students():
        q = request.args.get("q", "").strip()
        like = f"%{q}%"
        with db() as conn:
            rows = conn.execute(
                "SELECT * FROM students WHERE name LIKE ? OR email LIKE ? OR course LIKE ? ORDER BY id DESC",
                (like,
                 like,
                 like)).fetchall()
        return render_template("students.html", students=rows, q=q)

    def validate(form):
        name, email, course = (form.get(k, "").strip()
                               for k in ("name", "email", "course"))
        if not name or not email or not course:
            return None, "Please complete all required fields."
        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            return None, "Enter a valid email address."
        return {"name": name, "email": email.lower(), "course": course}, None

    @app.route("/students/add", methods=["GET", "POST"])
    def add_student():
        if request.method == "POST":
            data, error = validate(request.form)
            if error:
                flash(error, "error")
                return render_template(
                    "student_form.html",
                    student=None,
                    page_title="Add Student")
            try:
                with db() as conn:
                    conn.execute(
                        "INSERT INTO students(name,email,course) VALUES(?,?,?)",
                        (data["name"],
                         data["email"],
                            data["course"]))
                flash("Student added successfully.", "success")
                return redirect(url_for("students"))
            except sqlite3.IntegrityError:
                flash("That email address is already registered.", "error")
        return render_template(
            "student_form.html",
            student=None,
            page_title="Add Student")

    @app.route("/students/<int:sid>/edit", methods=["GET", "POST"])
    def edit_student(sid):
        with db() as conn:
            student = conn.execute(
                "SELECT * FROM students WHERE id=?", (sid,)).fetchone()
        if student is None:
            abort(404)
        if request.method == "POST":
            data, error = validate(request.form)
            if error:
                flash(error, "error")
            else:
                try:
                    with db() as conn:
                        conn.execute(
                            "UPDATE students SET name=?,email=?,course=? WHERE id=?",
                            (data["name"],
                             data["email"],
                                data["course"],
                                sid))
                    flash("Student updated successfully.", "success")
                    return redirect(url_for("students"))
                except sqlite3.IntegrityError:
                    flash(
                        "That email address is already registered to another student.",
                        "error")
        return render_template(
            "student_form.html",
            student=student,
            page_title="Edit Student")

    @app.post("/students/<int:sid>/delete")
    def delete_student(sid):
        with db() as conn:
            result = conn.execute("DELETE FROM students WHERE id=?", (sid,))
            if result.rowcount == 0:
                abort(404)
        flash("Student deleted successfully.", "success")
        return redirect(url_for("students"))

    # JSON API routes retained for CI/CD checks and integrations.
    @app.get("/api/health")
    def health():
        return jsonify(
            message="Student Management System is running",
            status="success")

    @app.route("/api/students", methods=["GET", "POST"])
    def api_students():
        if request.method == "GET":
            with db() as conn:
                rows = conn.execute(
                    "SELECT * FROM students ORDER BY id DESC").fetchall()
            return jsonify([dict(r) for r in rows])
        if not request.is_json:
            return jsonify(error="Content-Type must be application/json"), 400
        data, error = validate(request.get_json(silent=True) or {})
        if error:
            return jsonify(error=error), 400
        try:
            with db() as conn:
                cur = conn.execute(
                    "INSERT INTO students(name,email,course) VALUES(?,?,?)",
                    (data["name"],
                     data["email"],
                        data["course"]))
                sid = cur.lastrowid
            return jsonify(id=sid, **data), 201
        except sqlite3.IntegrityError:
            return jsonify(error="Email already exists"), 409

    @app.errorhandler(404)
    def not_found(_):
        return render_template("404.html"), 404
    return app


app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
