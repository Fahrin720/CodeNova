from flask import Blueprint, request, jsonify, session
from backend.db import supabase

products_bp = Blueprint('products', __name__)

# --- EXISTING ROUTES ---
@products_bp.route('/my-listings', methods=['GET'])
def get_my_listings():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    # Fetch only products where seller_id matches the logged-in user
    response = supabase.table("products").select("*").eq("seller_id", session['user_id']).execute()
    return jsonify(response.data), 200

@products_bp.route('/status/<product_id>', methods=['PATCH'])
def update_product_status(product_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.get_json()
    # Update the status in the 11-table database
    response = supabase.table("products").update({"status": data.get('status')}).eq("product_id", product_id).eq("seller_id", session['user_id']).execute()
    return jsonify(response.data), 200

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
        "description": data.get('description'),
        "status": "available"
    }).execute()
    
    return jsonify({"message": "Product listed!", "product": response.data[0]}), 201

# --- NEW PROFESSIONAL SEARCH & FILTER ROUTES ---

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    # Fetches all categories for your sidebar filter
    response = supabase.table("categories").select("*").execute()
    return jsonify(response.data), 200

@products_bp.route('/search', methods=['GET'])
def search_products():
    # 1. Get query parameters from the URL
    search_query = request.args.get('q', '')
    category_id = request.args.get('cat', 'all')
    sort_order = request.args.get('sort', 'newest')

    # 2. Start building the Supabase query
    query = supabase.table("products").select("*").eq("status", "available")

    # 3. Apply Text Search (Title or Description)
    if search_query:
        query = query.ilike("title", f"%{search_query}%")

    # 4. Apply Category Filter
    # Note: This assumes you have a category_id column in your products table
    if category_id != 'all':
        query = query.eq("category_id", category_id)

    # 5. Apply Sorting Logic
    if sort_order == 'price_low':
        query = query.order("price", ascending=True)
    elif sort_order == 'price_high':
        query = query.order("price", ascending=False)
    else:
        query = query.order("created_at", ascending=False)

    # 6. Execute and return
    response = query.execute()
    return jsonify(response.data), 200