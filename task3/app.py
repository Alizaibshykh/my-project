from pathlib import Path
import os
import sqlite3
from functools import wraps
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "development-only-change-this-secret")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
JWTManager(app)
DB = Path(__file__).with_name("employees.db")

def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, role TEXT NOT NULL CHECK(role IN ('employee','administrator')))")
        conn.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, department TEXT NOT NULL, email TEXT UNIQUE NOT NULL)")
        if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            conn.executemany("INSERT INTO users (username,password_hash,role) VALUES (?,?,?)", [
                ("employee1", generate_password_hash("Employee@123"), "employee"),
                ("admin1", generate_password_hash("Admin@123"), "administrator")
            ])
        if conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0] == 0:
            conn.executemany("INSERT INTO employees (name,department,email) VALUES (?,?,?)", [
                ("Ahmed Ali","Computer Science","ahmed@example.com"),
                ("Sara Khan","Administration","sara@example.com")
            ])

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        if get_jwt().get("role") != "administrator":
            return jsonify({"error": "Administrator role required"}), 403
        return fn(*args, **kwargs)
    return wrapper

def validate(data, partial=False):
    if not isinstance(data, dict):
        return None, "JSON object required"
    result = {}
    for field in ("name","department","email"):
        value = data.get(field)
        if value is None and partial:
            continue
        if not isinstance(value, str) or not value.strip():
            return None, f"{field} is required"
        result[field] = value.strip()
    if "email" in result and ("@" not in result["email"] or "." not in result["email"].split("@")[-1]):
        return None, "A valid email is required"
    return result, None

@app.get("/")
def home():
    return jsonify({"message": "Employee Management API", "login": "POST /login"})

@app.post("/login")
def login():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400
    username, password = data.get("username"), data.get("password")
    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"error": "Username and password are required"}), 400
    with connect() as conn:
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    if user is None or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid username or password"}), 401
    token = create_access_token(identity=user["username"], additional_claims={"role": user["role"]})
    return jsonify({"message": "Login successful", "access_token": token, "role": user["role"]})

@app.get("/employees")
@jwt_required()
def get_employees():
    with connect() as conn:
        rows = conn.execute("SELECT * FROM employees ORDER BY id").fetchall()
    return jsonify([dict(row) for row in rows])

@app.get("/employees/<int:pk>")
@jwt_required()
def get_employee(pk):
    with connect() as conn:
        row = conn.execute("SELECT * FROM employees WHERE id=?", (pk,)).fetchone()
    if row is None:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify(dict(row))

@app.post("/employees")
@admin_required
def add_employee():
    data, error = validate(request.get_json(silent=True))
    if error:
        return jsonify({"error": error}), 400
    try:
        with connect() as conn:
            cur = conn.execute("INSERT INTO employees (name,department,email) VALUES (?,?,?)", (data["name"],data["department"],data["email"]))
            row = conn.execute("SELECT * FROM employees WHERE id=?", (cur.lastrowid,)).fetchone()
        return jsonify(dict(row)), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

@app.put("/employees/<int:pk>")
@admin_required
def update_employee(pk):
    data, error = validate(request.get_json(silent=True), partial=True)
    if error:
        return jsonify({"error": error}), 400
    if not data:
        return jsonify({"error": "Provide at least one field"}), 400
    try:
        with connect() as conn:
            old = conn.execute("SELECT * FROM employees WHERE id=?", (pk,)).fetchone()
            if old is None:
                return jsonify({"error": "Employee not found"}), 404
            values = {k: data.get(k, old[k]) for k in ("name","department","email")}
            conn.execute("UPDATE employees SET name=?,department=?,email=? WHERE id=?", (values["name"],values["department"],values["email"],pk))
            row = conn.execute("SELECT * FROM employees WHERE id=?", (pk,)).fetchone()
        return jsonify(dict(row))
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

@app.delete("/employees/<int:pk>")
@admin_required
def delete_employee(pk):
    with connect() as conn:
        cur = conn.execute("DELETE FROM employees WHERE id=?", (pk,))
    if cur.rowcount == 0:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify({"message": "Employee deleted successfully"})

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5003, debug=True)
