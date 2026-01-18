from functools import wraps
from flask import session, jsonify

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Checks if the user_id exists in the current session
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized. Please log in first."}), 401
        return f(*args, **kwargs)
    return wrapper