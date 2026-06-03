from flask import Flask, request, jsonify
import sqlite3
import ast

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
    return "Hello from ReverseFlash Secure App"

@app.route('/search', methods=['GET'])
def search():
    # INTENTIONAL VULNERABILITY: SQL Injection (bandit: B608)
    query = request.args.get('q', '')
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    # Unsafe raw string formatting directly into the query
    raw_query = f"SELECT * FROM users WHERE username = '{query}'"
    
    try:
        cursor.execute(raw_query)
        results = cursor.fetchall()
    except Exception as e:
        results = str(e)
    finally:
        conn.close()
        
    return jsonify({"query_executed": raw_query, "results": results})

@app.route('/login', methods=['POST'])
def login():
    # INTENTIONAL VULNERABILITY: Hardcoded credentials (bandit: B105)
    ADMIN_USER = "admin"
    ADMIN_PASS = "SuperSecretPassword123!"
    
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    
    if username == ADMIN_USER and password == ADMIN_PASS:
        # INTENTIONAL VULNERABILITY: Unsafe eval() execution (bandit: B307)
        extra_command = data.get('extra_command', '1+1')
        try:
            eval_result = ast.literal_eval(extra_command)
        except Exception as e:
            eval_result = str(e)
            
        return jsonify({"status": "success", "admin_portal": True, "eval_result": eval_result})
    
    return jsonify({"status": "failure"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
