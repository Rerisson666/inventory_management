import sqlite3

def add_product(name, category, quantity, price, location):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO products (name, category, quantity, price, location)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, category, quantity, price, location))

    conn.commit()
    conn.close()

def update_stock(product_id, quantity_change):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE products
    SET quantity = quantity + ?
    WHERE id = ?
    ''', (quantity_change, product_id))

    conn.commit()
    conn.close()

def get_product_location(product_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT location FROM products
    WHERE id = ?
    ''', (product_id,))
    
    location = cursor.fetchone()
    conn.close()
    return location

def generate_report():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT name, quantity FROM products
    WHERE quantity < 10
    ''')

    low_stock = cursor.fetchall()

    cursor.execute('''
    SELECT name, quantity FROM products
    WHERE quantity > 100
    ''')

    high_stock = cursor.fetchall()

    cursor.execute('''
    SELECT name, quantity FROM products
    ''')

    all_products = cursor.fetchall()

    conn.close()
    return low_stock, high_stock, all_products
