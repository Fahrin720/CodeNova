from flask import Flask
from flask_cors import CORS
from backend.auth.routes import auth_bp
from backend.products.routes import products_bp
from backend.chats.routes import chats_bp
from backend.reviews.routes import reviews_bp

app = Flask(__name__)
CORS(app)
app.secret_key = "college_marketplace_secret_2026"

# Register ALL folders
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(chats_bp, url_prefix='/api/chats')
app.register_blueprint(reviews_bp, url_prefix='/api/reviews')

if __name__ == '__main__':
    app.run(debug=True, port=5000)