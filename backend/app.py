from flask import Flask, render_template

# We added 'template_folder' and 'static_folder' here.
# '../frontend' tells Flask: "Go up one folder, then look inside the frontend folder"
app = Flask(__name__, 
            template_folder='../frontend',
            static_folder='../frontend')

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/marketplace.html')
def marketplace():
    return render_template('marketplace.html')

@app.route('/services.html')
def services():
    return render_template('services.html')

@app.route('/laundry.html')
def laundry():
    return render_template('laundry.html')

@app.route('/cafe.html')
def cafe():
    return render_template('cafe.html')

@app.route('/news.html')
def news():
    return render_template('news.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html')

@app.route('/add-product.html')
def add_product():
    return render_template('add-product.html')

if __name__ == '__main__':
    # Run the server on port 5000
    app.run(debug=True, port=5000)