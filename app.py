from flask import Flask, request, render_template, redirect, url_for, flash
from inventory import add_product, update_stock, get_product_location, generate_report
from database import initialize_db, get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Substitua por uma chave secreta real

# Função para inicializar o banco de dados
def setup_database():
    initialize_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product_route():
    if request.method == 'POST':
        try:
            name = request.form['name']
            category = request.form['category']
            quantity = int(request.form['quantity'])
            price = float(request.form['price'])
            location = request.form['location']

            if not (name and category and quantity and price and location):
                flash('Todos os campos são obrigatórios!', 'error')
                return redirect(url_for('add_product_route'))

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO products (name, category, quantity, price, location) VALUES (?, ?, ?, ?, ?)',
                           (name, category, quantity, price, location))
            conn.commit()
            conn.close()

            flash('Produto adicionado com sucesso!', 'success')
        except Exception as e:
            print(f'Erro: {e}')
            flash('Ocorreu um erro ao adicionar o produto. Por favor, tente novamente.', 'error')
        return redirect(url_for('add_product_route'))

    return render_template('add_product.html')

@app.route('/update_stock', methods=['GET', 'POST'])
def update_stock_route():
    if request.method == 'POST':
        try:
            product_id = int(request.form['product_id'])
            quantity_change = int(request.form['quantity_change'])
            update_stock(product_id, quantity_change)
            flash('Estoque atualizado com sucesso!', 'success')
        except Exception as e:
            print(f'Erro: {e}')
            flash('Ocorreu um erro ao atualizar o estoque. Por favor, tente novamente.', 'error')
        return redirect(url_for('index'))
    return render_template('update_stock.html')

@app.route('/track_location', methods=['GET', 'POST'])
def track_location_route():
    location = None
    if request.method == 'POST':
        try:
            product_id = int(request.form['product_id'])
            location = get_product_location(product_id)
        except Exception as e:
            print(f'Erro: {e}')
            flash('Ocorreu um erro ao rastrear a localização. Por favor, tente novamente.', 'error')
    return render_template('track_location.html', location=location)

@app.route('/reports')
def reports():
    try:
        low_stock, high_stock, all_products = generate_report()
    except Exception as e:
        print(f'Erro: {e}')
        flash('Ocorreu um erro ao gerar o relatório. Por favor, tente novamente.', 'error')
        low_stock, high_stock, all_products = [], [], []
    return render_template('reports.html', low_stock=low_stock, high_stock=high_stock, all_products=all_products)

if __name__ == '__main__':
    setup_database()  # Inicializa o banco de dados antes de iniciar o servidor
    app.run(debug=True)
