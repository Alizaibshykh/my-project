from pathlib import Path
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB = Path(__file__).with_name("students.db")

def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT NOT NULL UNIQUE, name TEXT NOT NULL, department TEXT NOT NULL, email TEXT NOT NULL UNIQUE)")

def payload(partial=False):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, "Request body must be a JSON object"
    result = {}
    for field in ("student_id", "name", "department", "email"):
        value = data.get(field)
        if value is None and partial:
            continue
        if not isinstance(value, str) or not value.strip():
            return None, f"{field} is required and must be a non-empty string"
        result[field] = value.strip()
    if "email" in result and ("@" not in result["email"] or "." not in result["email"].split("@")[-1]):
        return None, "A valid email address is required"
    return result, None

@app.get("/")
def home():
    return jsonify({"message": "Student Management API"})

@app.get("/students")
def all_students():
    with connect() as conn:
        rows = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    return jsonify([dict(row) for row in rows])

@app.get("/students/<int:pk>")
def one_student(pk):
    with connect() as conn:
        row = conn.execute("SELECT * FROM students WHERE id=?", (pk,)).fetchone()
    if row is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(row))

@app.post("/students")
def add_student():
    data, error = payload()
    if error:
        return jsonify({"error": error}), 400
    try:
        with connect() as conn:
            cur = conn.execute("INSERT INTO students (student_id,name,department,email) VALUES (?,?,?,?)", (data["student_id"],data["name"],data["department"],data["email"]))
            row = conn.execute("SELECT * FROM students WHERE id=?", (cur.lastrowid,)).fetchone()
        return jsonify(dict(row)), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Student ID or email already exists"}), 409

@app.put("/students/<int:pk>")
def edit_student(pk):
    data, error = payload(partial=True)
    if error:
        return jsonify({"error": error}), 400
    if not data:
        return jsonify({"error": "Provide at least one field to update"}), 400
    try:
        with connect() as conn:
            old = conn.execute("SELECT * FROM students WHERE id=?", (pk,)).fetchone()
            if old is None:
                return jsonify({"error": "Student not found"}), 404
            values = {k: data.get(k, old[k]) for k in ("student_id","name","department","email")}
            conn.execute("UPDATE students SET student_id=?,name=?,department=?,email=? WHERE id=?", (values["student_id"],values["name"],values["department"],values["email"],pk))
            row = conn.execute("SELECT * FROM students WHERE id=?", (pk,)).fetchone()
        return jsonify(dict(row))
    except sqlite3.IntegrityError:
        return jsonify({"error": "Student ID or email already exists"}), 409

@app.delete("/students/<int:pk>")
def remove_student(pk):
    with connect() as conn:
        cur = conn.execute("DELETE FROM students WHERE id=?", (pk,))
    if cur.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "Student deleted successfully"})

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5001, debug=True)
