from flask import Blueprint, request, jsonify, session
from backend.db import supabase
from backend.utils.auth_guard import login_required

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/add', methods=['POST'])
@login_required
def add_review():
    data = request.get_json()
    # Ensure rating is between 1 and 5 as per your SQL schema
    rating = data.get('rating')
    if not (1 <= rating <= 5):
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    response = supabase.table("reviews").insert({
        "order_item_id": data.get('order_item_id'),
        "reviewer_id": session['user_id'],
        "rating": rating,
        "comment": data.get('comment')
    }).execute()
    return jsonify(response.data[0]), 201