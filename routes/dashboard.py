from flask import render_template,request,jsonify
from app import app
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/admin')
@app.route('/')
def dashboard():  # put application's code here
    module = 'dashboard'
    return render_template('admin/dashboard.html', module=module)


@app.route('/user')
def user():  # put application's code here
    module = 'user'
    return render_template('admin/user.html', module=module)


@app.route('/admin/table')
def table():  # put application's code here
    module = 'table'
    return render_template('admin/table.html', module=module)


@app.route('/admin/profile')
def profile():  # put application's code here
    module = 'profile'
    return render_template('admin/profile.html', module=module)


@app.route('/admin/billing')
def billing():  # put application's code here
    module = 'billing'
    return render_template('admin/billing.html', module=module)


@app.route('/admin/user')
def user_x():  # put application's code here
    module = 'user'
    return render_template('admin/user.html', module=module)


@app.route('/admin/category')
def category():  # put application's code here
    module = 'category'
    return render_template('admin/category.html', module=module)


# Get all categories
@app.route('/categories')
def get_categories():
    try:
        conn = get_db_connection()
        categories = conn.execute('SELECT * FROM categories').fetchall()
        conn.close()

        categories_list = [
            {'id': category['id'], 'name': category['name'], 'description': category['description']}
            for category in categories
        ]
        
        return jsonify(categories_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_category', methods=['POST'])
def add_category():
    data = request.json
    
    # Validate input data
    name = data.get('name')
    description = data.get('description')
    
    if not name or not description:
        return jsonify({'status': 'error', 'message': 'Name and description are required.'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO categories (name, description) VALUES (?, ?)',
            (name, description)
        )
        conn.commit()

        new_category_id = cursor.lastrowid
        conn.close()

        # Return success status with the new category ID
        return jsonify({'status': 'success', 'id': new_category_id}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/delete_category/<int:id>', methods=['DELETE'])
def delete_category(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM categories WHERE id = ?', (id,))
        conn.commit()
        conn.close()

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/edit_category', methods=['GET'])
def edit_category():
    # Get the category ID from the request arguments
    category_id = request.args.get('id')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute a query to fetch the category with the specified ID
    cursor.execute("SELECT * FROM categories WHERE id=?", (category_id,))
    row = cursor.fetchone()
    conn.close()
    
    # Check if the category was found
    if row:
        current_category = {
            'id': row['id'],
            'name': row['name'],
            'description': row['description'],
        }
        return jsonify(current_category), 200  # Return the category as JSON
    else:
        return jsonify({row: "Category not found "}), 404  # Return a 404 error if not found


@app.route('/update_category/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.json

    # Validate input data
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({'status': 'error', 'message': 'Name and description are required.'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE categories SET name = ?, description = ? WHERE id = ?',
            (name, description, id)
        )
        conn.commit()
        conn.close()

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/products')
def get_products():
    try:
        conn = get_db_connection()
        products = conn.execute('SELECT * FROM products').fetchall()
        conn.close()

        product_list = [
            {
                'id': product['id'],
                'code': product['code'],
                'image': product['image'],
                'name': product['name'],
                'category': product['category'],
                'cost': product['cost'],
                'price': product['price'],
                'current_stock': product['current_stock']
            } for product in products
        ]

        return jsonify(product_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Add new product
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    code = data.get('code')
    image = data.get('image')
    name = data.get('name')
    category = data.get('category')
    cost = data.get('cost')
    price = data.get('price')
    current_stock = data.get('current_stock')
    
    if not all([code, name, category, cost, price, current_stock]):
        return jsonify({'status': 'error', 'message': 'All fields are required.'}), 400
    
    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO products (code, image, name, category, cost, price, current_stock) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (code, image, name, category, cost, price, current_stock)
        )
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Update product
@app.route('/update_product/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    name = data.get('name')
    code = data.get('code')
    image = data.get('image')
    category = data.get('category')
    cost = data.get('cost')
    price = data.get('price')
    current_stock = data.get('current_stock')
    
    if not all([code, name, category, cost, price, current_stock]):
        return jsonify({'status': 'error', 'message': 'All fields are required.'}), 400
    
    try:
        conn = get_db_connection()
        conn.execute(
            'UPDATE products SET code=?, image=?, name=?, category=?, cost=?, price=?, current_stock=? WHERE id=?',
            (code, image, name, category, cost, price, current_stock, id)
        )
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Delete product
@app.route('/delete_product/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM products WHERE id=?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/admin/product')
def product():  # put application's code here
    module = 'product'
    return render_template('admin/product.html', module=module)