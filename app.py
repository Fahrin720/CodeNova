import os
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session

# Standard Flask setup. 
# It automatically looks for a 'templates' folder and a 'static' folder.
app = Flask(__name__) 

app.secret_key = 'kmlife_ultra_secret_2026'

# --- 1. MOCK DATABASE ---
users = {
    "2024111": {
        "student_id": "2024111", "name": "Ariff Syahmi", "password": "123", 
        "role": "admin", "room": "E302", "blok": "E", "coins": 150, "vouches": 14
    }
}

# --- 2. ACCESS CONTROL ---
@app.before_request
def force_login():
    # Allow static files (CSS/Images) to load automatically
    if request.path.startswith('/static'):
        return

    allowed_routes = ['login_page', 'signup_page', 'handle_login', 'handle_signup']
    if 'user_id' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('login_page'))

@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    curr_user = users.get(user_id) if user_id else None
    return dict(user=curr_user)

# --- 3. ROUTES ---
@app.route('/')
def home_page(): return render_template('index.html')

@app.route('/login')
def login_page():
    if 'user_id' in session: return redirect(url_for('home_page'))
    return render_template('login.html')

@app.route('/signup')
def signup_page(): return render_template('signup.html')

@app.route('/marketplace')
def marketplace_page(): return render_template('marketplace.html')

@app.route('/services')
def services_page(): return render_template('services.html')

@app.route('/laundry')
def laundry_page(): return render_template('laundry.html')

@app.route('/cafe')
def cafe_page(): return render_template('cafe.html')

@app.route('/news')
def news_page(): return render_template('news.html')

@app.route('/profile')
def profile_page(): return render_template('profile.html')

# --- 4. ACTION LOGIC ---
@app.route('/api/auth/login', methods=['POST'])
def handle_login():
    sid = request.form.get('student_id')
    pw = request.form.get('password')
    if sid in users and users[sid]['password'] == pw:
        session['user_id'] = sid
        return redirect(url_for('home_page'))
    return "<h1>Login Failed</h1><a href='/login'>Try again</a>", 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)