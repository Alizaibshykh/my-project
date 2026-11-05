from pathlib import Path
import hashlib
import secrets
import sqlite3
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
HERE = Path(__file__).resolve().parent
DB = HERE / "apikeys.db"
SECRET_DIR = HERE / "secrets"
KEY_FILE = SECRET_DIR / "api_keys.txt"

def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def digest(key):
    return hashlib.sha256(key.encode("utf-8")).hexdigest()

def init_keys():
    SECRET_DIR.mkdir(exist_ok=True)
    with connect() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS api_keys (id INTEGER PRIMARY KEY AUTOINCREMENT, consumer TEXT UNIQUE NOT NULL, key_hash TEXT UNIQUE NOT NULL, is_active INTEGER NOT NULL DEFAULT 1)")
        count = conn.execute("SELECT COUNT(*) FROM api_keys").fetchone()[0]
        if count == 0:
            generated = []
            for consumer in ("Consumer 1", "Consumer 2", "Consumer 3"):
                key = secrets.token_urlsafe(32)
                generated.append((consumer, key))
                conn.execute("INSERT INTO api_keys (consumer,key_hash) VALUES (?,?)", (consumer,digest(key)))
            with KEY_FILE.open("w", encoding="utf-8") as output:
                output.write("PRIVATE CLASSROOM KEYS – DO NOT COMMIT THIS FILE\n\n")
                for consumer, key in generated:
                    output.write(f"{consumer}: {key}\n")
            try:
                os.chmod(KEY_FILE, 0o600)
            except OSError:
                pass
        elif not KEY_FILE.exists():
            print("WARNING: plaintext key file missing. Restore it from your private backup or reset apikeys.db to generate new keys.")

def key_is_valid(key):
    if not key:
        return False
    with connect() as conn:
        row = conn.execute("SELECT id FROM api_keys WHERE key_hash=? AND is_active=1", (digest(key),)).fetchone()
    return row is not None

@app.get("/")
def home():
    return jsonify({"message": "Text Processing API", "endpoint": "POST /process"})

@app.post("/process")
def process():
    if not key_is_valid(request.headers.get("X-API-Key")):
        return jsonify({"error": "Missing or invalid API key"}), 401
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400
    text = data.get("text")
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "A non-empty text string is required"}), 400
    return jsonify({"original_text": text, "processed_text": text.upper()})

if __name__ == "__main__":
    init_keys()
    print(f"Private API key file: {KEY_FILE}")
    app.run(host="127.0.0.1", port=5002, debug=True)
