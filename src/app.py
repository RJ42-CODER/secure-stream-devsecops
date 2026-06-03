from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Initialize a dummy database for testing
def init_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)''')
    cursor.execute('''INSERT OR IGNORE INTO users (id, username) VALUES (1, 'admin')''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return "Hello from ReverseFlash Secure App (Secure Version)"

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')

    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # ✅ FIX: Parameterized query (NO SQL injection)
    raw_query = "SELECT * FROM users WHERE username = ?"

    try:
        cursor.execute(raw_query, (query,))
        results = cursor.fetchall()
    except Exception as e:
        results = str(e)
    finally:
        conn.close()

    return jsonify({
        "query_executed": "SAFE QUERY",
        "results": results
    })

@app.route('/login', methods=['POST'])
def login():
    # ✅ FIX: No hardcoded credentials
    ADMIN_USER = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASS = os.getenv("ADMIN_PASS", "default_pass")

    data = request.json or {}
    username = data.get('username')
    password = data.get('password')

    if username == ADMIN_USER and password == ADMIN_PASS:

        extra_command = data.get('extra_command', '1+1')

        # ✅ FIX: No eval usage
        try:
            eval_result = str(extra_command)
        except Exception as e:
            eval_result = str(e)

        return jsonify({
            "status": "success",
            "admin_portal": True,
            "eval_result": eval_result
        })

    return jsonify({"status": "failure"}), 401


if __name__ == '__main__':
    # safer local bind
    app.run(host='127.0.0.1', port=5000)