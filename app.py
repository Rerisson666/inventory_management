from flask import Flask, request, render_template, redirect, url_for
from inventory import add_product, update_stock, get_product_location, generate_report
from database import initialize_db

app = Flask(__name__)

# Função para inicializar o banco de dados
def setup_database():
    initialize_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product_route():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        location = request.form['location']
        add_product(name, category, quantity, price, location)
        return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/update_stock', methods=['GET', 'POST'])
def update_stock_route():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        quantity_change = int(request.form['quantity_change'])
        update_stock(product_id, quantity_change)
        return redirect(url_for('index'))
    return render_template('update_stock.html')

@app.route('/track_location', methods=['GET', 'POST'])
def track_location_route():
    location = None
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        location = get_product_location(product_id)
    return render_template('track_location.html', location=location)

@app.route('/reports')
def reports():
    low_stock, high_stock, all_products = generate_report()
    return render_template('reports.html', low_stock=low_stock, high_stock=high_stock, all_products=all_products)

if __name__ == '__main__':
    setup_database()  # Inicializa o banco de dados antes de iniciar o servidor
    app.run(debug=True)