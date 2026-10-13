
from flask import Flask, request, jsonify

app = Flask(__name__)

students = []
next_id = 1


@app.get("/")
def home():
    return jsonify({
        "message": "Student Management System is running",
        "status": "success"
    })


@app.get("/students")
def get_students():
    return jsonify(students), 200


@app.post("/students")
def add_student():
    global next_id

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    name = data.get("name")
    email = data.get("email")
    course = data.get("course")

    if not all(
        isinstance(value, str) and value.strip()
        for value in (name, email, course)
    ):
        return jsonify({
            "error": "Name, email and course are required"
        }), 400

    student = {
        "id": next_id,
        "name": name.strip(),
        "email": email.strip(),
        "course": course.strip()
    }

    students.append(student)
    next_id += 1

    return jsonify(student), 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
