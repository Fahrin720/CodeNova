from flask import Blueprint, request, jsonify, session
from backend.db import supabase

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_all_products():
    # Fetch available items from Supabase
    response = supabase.table("products").select("*").eq("status", "available").execute()
    return jsonify(response.data), 200

@products_bp.route('/add', methods=['POST'])
def add_product():
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401
    
    data = request.get_json()
    response = supabase.table("products").insert({
        "seller_id": session['user_id'],
        "title": data.get('title'),
        "price": data.get('price'),
        "description": data.get('description')
    }).execute()
    
    return jsonify({"message": "Product listed!", "product": response.data[0]}), 201