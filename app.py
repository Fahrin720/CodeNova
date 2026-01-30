import os
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__) 
app.secret_key = 'kmlife_ultra_secret_2026'

# ==========================================================================
# 1. EXPANDED MOCK DATABASE
# ==========================================================================
users = {
    "2024111": {
        "student_id": "2024111", "name": "Ariff Syahmi", "password": "123", 
        "role": "admin", "room": "E302", "blok": "E", "coins": 150, "vouches": 14,
        "creator_status": "approved"
    }
}

# New Marketplace Items
listings = [
    {
        "id": 1, "title": "Calculus 1 Textbook", "price": 35, 
        "seller": "Ariff (E302)", "status": "urgent", "cat": "Books", 
        "img": "/static/img/kmlimage.jpg", "desc": "Good condition, no highlights."
    },
    {
        "id": 2, "title": "Nasi Lemak Ayam", "price": 5, 
        "seller": "Fahrin (F101)", "status": "nego", "cat": "Food", 
        "img": "/static/img/nasilemak.jpeg", "desc": "Extra spicy sambal!"
    }
]

# New Laundry Status logic
def get_laundry_data():
    return {
        "Dryers": [
            {"id": "D1", "status": "busy", "user": "Ziq (E104)", "time_left": 15},
            {"id": "D2", "status": "available", "user": "-", "time_left": 0},
            {"id": "D3", "status": "available", "user": "-", "time_left": 0}
        ],
        "Washers": [
            {"id": "W1", "status": "busy", "user": "Ariff (E302)", "time_left": 35},
            {"id": "W2", "status": "available", "user": "-", "time_left": 0},
            {"id": "W3", "status": "available", "user": "-", "time_left": 0},
            # ... and so on
        ]
    }

# ==========================================================================
# 2. SECURITY & CONTEXT
# ==========================================================================
@app.before_request
def force_login():
    if request.path.startswith('/static') or request.path.endswith(('.css', '.js', '.jpg', '.png', '.jpeg')):
        return
    allowed = ['login_page', 'signup_page', 'handle_login', 'handle_signup']
    if 'user_id' not in session and request.endpoint not in allowed:
        return redirect(url_for('login_page'))

@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    return dict(user=users.get(user_id))

# ==========================================================================
# 3. DYNAMIC ROUTES (Passing data to HTML)
# ==========================================================================

@app.route('/')
def home_page():
    # Pass only the first 3 listings for the 'New in Marketplace' preview
    return render_template('index.html', recent_items=listings[:3])

@app.route('/marketplace')
def marketplace_page():
    # Pass ALL items to the marketplace
    return render_template('marketplace.html', items=listings)

@app.route('/laundry')
def laundry_page():
    data = get_laundry_data()
    return render_template('laundry.html', machines=data)

# ... (Keep other routes like /profile, /cafe, /news the same)

# ==========================================================================
# 4. ACTION APIs
# ==========================================================================

@app.route('/api/auth/login', methods=['POST'])
def handle_login():
    sid = request.form.get('student_id')
    pw = request.form.get('password')
    if sid in users and users[sid]['password'] == pw:
        session['user_id'] = sid
        return redirect(url_for('home_page'))
    return "Login Failed", 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)