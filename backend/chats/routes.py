from flask import Blueprint, request, jsonify, session
from backend.db import supabase
from backend.utils.auth_guard import login_required

chats_bp = Blueprint('chats', __name__)

@chats_bp.route('/create', methods=['POST'])
@login_required
def create_chat():
    data = request.get_json()
    # Logic to start a new chat linked to a specific product
    response = supabase.table("chats").insert({
        "product_id": data.get('product_id'),
        "buyer_id": session['user_id'],
        "seller_id": data.get('seller_id')
    }).execute()
    return jsonify(response.data[0]), 201

@chats_bp.route('/message', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    response = supabase.table("messages").insert({
        "chat_id": data.get('chat_id'),
        "sender_id": session['user_id'],
        "message_text": data.get('message_text')
    }).execute()
    return jsonify(response.data[0]), 201