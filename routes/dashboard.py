from flask import render_template, request, jsonify
from app import app
import sqlite3
from werkzeug.utils import secure_filename
import os
from PIL import Image

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


# @app.route('/admin/user')
# def user_x():  # put application's code here
#     module = 'user'
#     return render_template('admin/user.html', module=module)


# @app.route('/admin/category')
# def category():  # put application's code here
#     module = 'category'
#     return render_template('admin/category.html', module=module)


# Get all categories
# @app.route('/categories')
# def get_categories():
#     try:
#         conn = get_db_connection()
#         categories = conn.execute('SELECT * FROM categories').fetchall()
#         conn.close()
#
#         categories_list = [
#             {'id': category['id'], 'name': category['name'], 'description': category['description']}
#             for category in categories
#         ]
#
#         return jsonify(categories_list), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
# @app.route('/add_category', methods=['POST'])
# def add_category():
#     data = request.json
#
#     # Validate input data
#     name = data.get('name')
#     description = data.get('description')
#
#     if not name or not description:
#         return jsonify({'status': 'error', 'message': 'Name and description are required.'}), 400
#
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             'INSERT INTO categories (name, description) VALUES (?, ?)',
#             (name, description)
#         )
#         conn.commit()
#
#         new_category_id = cursor.lastrowid
#         conn.close()
#
#         # Return success status with the new category ID
#         return jsonify({'status': 'success', 'id': new_category_id}), 201
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500
#
#
# @app.route('/delete_category/<int:id>', methods=['DELETE'])
# def delete_category(id):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute('DELETE FROM categories WHERE id = ?', (id,))
#         conn.commit()
#         conn.close()
#
#         return jsonify({'status': 'success'}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500
#
# @app.route('/edit_category', methods=['GET'])
# def edit_category():
#     # Get the category ID from the request arguments
#     category_id = request.args.get('id')
#
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     # Execute a query to fetch the category with the specified ID
#     cursor.execute("SELECT * FROM categories WHERE id=?", (category_id,))
#     row = cursor.fetchone()
#     conn.close()
#
#     # Check if the category was found
#     if row:
#         current_category = {
#             'id': row['id'],
#             'name': row['name'],
#             'description': row['description'],
#         }
#         return jsonify(current_category), 200  # Return the category as JSON
#     else:
#         return jsonify({row: "Category not found "}), 404  # Return a 404 error if not found
#
#
# @app.route('/update_category/<int:id>', methods=['PUT'])
# def update_category(id):
#     data = request.json
#
#     # Validate input data
#     name = data.get('name')
#     description = data.get('description')
#
#     if not name or not description:
#         return jsonify({'status': 'error', 'message': 'Name and description are required.'}), 400
#
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             'UPDATE categories SET name = ?, description = ? WHERE id = ?',
#             (name, description, id)
#         )
#         conn.commit()
#         conn.close()
#
#         return jsonify({'status': 'success'}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500


# @app.route('/products')
# def get_products():
#     try:
#         conn = get_db_connection()
#         products = conn.execute('SELECT * FROM products').fetchall()
#         conn.close()
#
#         product_list = [
#             {
#                 'id': product['id'],
#                 'code': product['code'],
#                 # Update image path to point to the compressed image folder
#                 'image': f'/static/uploads/product/compress/{product["image"].split("/")[-1]}',
#                 'name': product['name'],
#                 'category': product['category'],
#                 'cost': product['cost'],
#                 'price': product['price'],
#                 'current_stock': product['current_stock']
#             } for product in products
#         ]
#
#         return jsonify(product_list), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
#
# @app.route('/product/fullphoto/<int:product_id>', methods=['GET'])
# def get_product_full_photo(product_id):
#     try:
#         conn = get_db_connection()
#         product = conn.execute('SELECT image FROM products WHERE id = ?', (product_id,)).fetchone()
#         conn.close()
#         if not product:
#             return jsonify({'error': 'Product not found'}), 404
#
#         full_photo_url = product["image"]
#         return jsonify({'image_url': full_photo_url}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
#
# # Add new product
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# @app.route('/add_product', methods=['POST'])
# def add_product():
#     if 'image' not in request.files:
#         return jsonify({'status': 'error', 'message': 'No image uploaded'}), 400
#
#     file = request.files['image']
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         # Define paths
#         original_path = f'/static/uploads/product/original/{filename}'
#         compress_path = f'/static/uploads/product/compress/{filename}'
#
#         # Remove leading slash for actual file saving
#         original_save_path = original_path[1:]  # Remove the leading slash for file system operations
#         compress_save_path = compress_path[1:]
#
#         # Full paths
#         original_full_path = os.path.join(os.getcwd(), original_save_path)
#         compress_full_path = os.path.join(os.getcwd(), compress_save_path)
#
#         # Ensure directories exist
#         os.makedirs(os.path.dirname(original_full_path), exist_ok=True)
#         os.makedirs(os.path.dirname(compress_full_path), exist_ok=True)
#
#         # Save the original file
#         file.save(original_full_path)
#
#         # Open the image for resizing
#         img = Image.open(file.stream)
#
#         # Resize the image to 30x30 for compression
#         img = img.resize((30, 30))
#
#         # Save the compressed image
#         img.save(compress_full_path)
#
#         # Retrieve form data
#         code = request.form.get('code')
#         name = request.form.get('name')
#         category = request.form.get('category')
#         cost = request.form.get('cost')
#         price = request.form.get('price')
#         current_stock = request.form.get('current_stock')
#
#         if not all([code, name, category, cost, price, current_stock]):
#             return jsonify({'status': 'error', 'message': 'All fields are required.'}), 400
#
#         try:
#             # Save the product details with both image paths
#             conn = get_db_connection()
#             conn.execute(
#                 'INSERT INTO products (code, image, name, category, cost, price, current_stock) VALUES (?, ?, ?, ?, ?, ?, ?)',
#                 (code, original_path, name, category, cost, price, current_stock)
#             )
#             conn.commit()
#             conn.close()
#             return jsonify({'status': 'success'}), 201
#         except Exception as e:
#             return jsonify({'status': 'error', 'message': str(e)}), 500
#     else:
#         return jsonify({'status': 'error', 'message': 'Invalid file type'}), 400
#
#
# @app.route('/update_product/<int:id>', methods=['PUT'])
# def update_product(id):
#     if 'image' in request.files:
#         file = request.files['image']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             # Define paths
#             original_path = f'/static/uploads/product/original/{filename}'
#             compress_path = f'/static/uploads/product/compress/{filename}'
#
#             # Remove leading slash for actual file saving
#             original_save_path = original_path[1:]
#             compress_save_path = compress_path[1:]
#
#             # Full paths
#             original_full_path = os.path.join(os.getcwd(), original_save_path)
#             compress_full_path = os.path.join(os.getcwd(), compress_save_path)
#
#             # Ensure directories exist
#             os.makedirs(os.path.dirname(original_full_path), exist_ok=True)
#             os.makedirs(os.path.dirname(compress_full_path), exist_ok=True)
#
#             # Save the original file
#             file.save(original_full_path)
#
#             # Open the image for resizing
#             img = Image.open(file)
#
#             # Resize the image to 30x30 for compression
#             img = img.resize((30, 30))
#
#             # Save the compressed image
#             img.save(compress_full_path)
#
#             image_path = original_path
#     else:
#         # If no new image is uploaded, keep the existing image
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute('SELECT image FROM products WHERE id = ?', (id,))
#         result = cursor.fetchone()
#         conn.close()
#         image_path = result['image'] if result else None
#
#     # Get form data
#     name = request.form.get('name')
#     code = request.form.get('code')
#     category = request.form.get('category')
#     cost = request.form.get('cost')
#     price = request.form.get('price')
#     current_stock = request.form.get('current_stock')
#
#     if not all([name, code]):
#         return jsonify({'status': 'error', 'message': 'Name and Code are required.'}), 400
#
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#
#         # Update the product in the database
#         cursor.execute('''
#             UPDATE products
#             SET name = ?,
#                 code = ?,
#                 image = ?,
#                 category = ?,
#                 cost = ?,
#                 price = ?,
#                 current_stock = ?
#             WHERE id = ?
#         ''', (name, code, image_path, category, cost, price, current_stock, id))
#
#         conn.commit()
#         conn.close()
#
#         return jsonify({'status': 'success'}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500
# # Delete product
# @app.route('/delete_product/<int:id>', methods=['DELETE'])
# def delete_product(id):
#     try:
#         conn = get_db_connection()
#         conn.execute('DELETE FROM products WHERE id=?', (id,))
#         conn.commit()
#         conn.close()
#         return jsonify({'status': 'success'}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500
#
# @app.route('/admin/product')
# def product():  # put application's code here
#     module = 'product'
#     return render_template('admin/product.html', module=module)
# # -------------user----------
# # Add new user
# @app.route('/add_user', methods=['POST'])
# def add_user():
#     data = request.json
#     code = data.get('code')
#     profile = data.get('profile')
#     name = data.get('name')
#     gender_id = data.get('gender_id')
#     role = data.get('role')
#     email = data.get('email')
#     phone = data.get('phone')
#     address = data.get('address')
#
#     if not all([code, name, email]):
#         return jsonify({'status': 'error', 'message': 'Code, name, and email are required.'}), 400
#
#     try:
#         conn = get_db_connection()
#         conn.execute(
#             'INSERT INTO Users (code, profile, name, gender_id, role, email, phone, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
#             (code, profile, name, gender_id, role, email, phone, address)
#         )
#         conn.commit()
#         conn.close()
#         return jsonify({'status': 'success'}), 201
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500
#
# # Update user
# @app.route('/update_user/<int:id>', methods=['PUT'])
# def update_user(id):
#     data = request.json
#     code = data.get('code')
#     profile = data.get('profile')
#     name = data.get('name')
#     gender_id = data.get('gender_id')
#     role = data.get('role')
#     email = data.get('email')
#     phone = data.get('phone')
#     address = data.get('address')
#
#     if not all([code, name, email]):
#         return jsonify({'status': 'error', 'message': 'Code, name, and email are required.'}), 400
#
#     try:
#         conn = get_db_connection()
#         conn.execute(
#             'UPDATE Users SET code = ?, profile = ?, name = ?, gender_id = ?, role = ?, email = ?, phone = ?, address = ? WHERE id = ?',
#             (code, profile, name, gender_id, role, email, phone, address, id)
#         )
#         conn.commit()
#         conn.close()
#         return jsonify({'status': 'success'}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500
#
# # Delete user
# @app.route('/delete_user/<int:id>', methods=['DELETE'])
# def delete_user(id):
#     try:
#         conn = get_db_connection()
#         conn.execute('DELETE FROM Users WHERE id = ?', (id,))
#         conn.commit()
#         conn.close()
#         return jsonify({'status': 'success'}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500
#
# # Get all users
# @app.route('/users', methods=['GET'])
# def get_users():
#     try:
#         conn = get_db_connection()
#         users = conn.execute('SELECT * FROM Users').fetchall()
#         conn.close()
#         return jsonify([dict(user) for user in users]), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500
#
# # Get user by ID
# @app.route('/user/<int:id>', methods=['GET'])
# def get_user(id):
#     try:
#         conn = get_db_connection()
#         user = conn.execute('SELECT * FROM Users WHERE id = ?', (id,)).fetchone()
#         conn.close()
#         if user:
#             return jsonify(dict(user)), 200
#         else:
#             return jsonify({'status': 'error', 'message': 'User not found'}), 404
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500