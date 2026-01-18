from flask import Blueprint, request, jsonify, session
from backend.db import supabase
from backend.utils.auth_guard import login_required

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    data = request.get_json()
    items = data.get('items') # Expecting a list of items

    if not items:
        return jsonify({"error": "No items in cart"}), 400

    try:
        # 1. Create the main Order
        order_response = supabase.table("orders").insert({
            "buyer_id": session['user_id'],
            "total_amount": data.get('total_amount'),
            "order_status": "pending"
        }).execute()
        
        new_order_id = order_response.data[0]['order_id']

        # 2. Add items to order_items table
        for item in items:
            supabase.table("order_items").insert({
                "order_id": new_order_id,
                "product_id": item['product_id'],
                "seller_id": item['seller_id'],
                "price_at_purchase": item['price'],
                "quantity": item.get('quantity', 1)
            }).execute()

        return jsonify({"message": "Order placed successfully!", "order_id": new_order_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@orders_bp.route('/history', methods=['GET'])
@login_required
def get_order_history():
    # Fetch all orders for the logged-in user
    response = supabase.table("orders").select("*").eq("buyer_id", session['user_id']).execute()
    return jsonify(response.data), 200