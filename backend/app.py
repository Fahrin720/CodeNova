from flask import Flask, request, jsonify, session
import mysql.connector
import bcrypt

# =========================
# APP SETUP
# =========================
app = Flask(__name__)
app.secret_key = "test_secret_key"

# =========================
# DATABASE CONNECTION
# (phpMyAdmin uses MySQL)
# =========================
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # phpMyAdmin username
        password="",          # phpMyAdmin password (empty if XAMPP default)
        database="college_marketplace"
    )

# =========================
# REGISTER
# =========================
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json

    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    if not full_name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (full_name, email, password_hash) VALUES (%s, %s, %s)",
            (full_name, email, hashed_pw)
        )
        db.commit()
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    finally:
        cursor.close()
        db.close()

    return jsonify({
        "success": True,
        "message": "User registered successfully"
    }), 201

# =========================
# LOGIN
# =========================
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
        return jsonify({"error": "Invalid credentials"}), 401

    session['user_id'] = user['user_id']

    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": {
            "id": user['user_id'],
            "name": user['full_name']
        }
    })

# =========================
# CHECK SESSION
# =========================
@app.route('/api/auth/me', methods=['GET'])
def me():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT user_id, full_name, email FROM users WHERE user_id = %s",
        (session['user_id'],)
    )
    user = cursor.fetchone()
    cursor.close()
    db.close()

    return jsonify(user)

# =========================
# LOGOUT
# =========================
@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})

# =========================
# ROOT
# =========================
@app.route('/')
def home():
    return "Flask + phpMyAdmin backend running ✅"

# =========================
# RUN SERVER
# =========================
if __name__ == '__main__':
    app.run(debug=True)
