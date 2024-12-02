import os
from PIL import Image
from flask import render_template, request, jsonify
from werkzeug.utils import secure_filename

from app import app
from routes.dashboard import get_db_connection, ALLOWED_EXTENSIONS


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
                # Update image path to point to the compressed image folder
                'image': f'/static/uploads/product/compress/{product["image"].split("/")[-1]}',
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


@app.route('/product/fullphoto/<int:product_id>', methods=['GET'])
def get_product_full_photo(product_id):
    try:
        conn = get_db_connection()
        product = conn.execute('SELECT image FROM products WHERE id = ?', (product_id,)).fetchone()
        conn.close()
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        full_photo_url = product["image"]
        return jsonify({'image_url': full_photo_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Add new product
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/add_product', methods=['POST'])
def add_product():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No image uploaded'}), 400

    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Define paths
        original_path = f'/static/uploads/product/original/{filename}'
        compress_path = f'/static/uploads/product/compress/{filename}'

        # Remove leading slash for actual file saving
        original_save_path = original_path[1:]  # Remove the leading slash for file system operations
        compress_save_path = compress_path[1:]

        # Full paths
        original_full_path = os.path.join(os.getcwd(), original_save_path)
        compress_full_path = os.path.join(os.getcwd(), compress_save_path)

        # Ensure directories exist
        os.makedirs(os.path.dirname(original_full_path), exist_ok=True)
        os.makedirs(os.path.dirname(compress_full_path), exist_ok=True)

        # Save the original file
        file.save(original_full_path)

        # Open the image for resizing
        img = Image.open(file.stream)

        # Resize the image to 30x30 for compression
        img = img.resize((30, 30))

        # Save the compressed image
        img.save(compress_full_path)

        # Retrieve form data
        code = request.form.get('code')
        name = request.form.get('name')
        category = request.form.get('category')
        cost = request.form.get('cost')
        price = request.form.get('price')
        current_stock = request.form.get('current_stock')

        if not all([code, name, category, cost, price, current_stock]):
            return jsonify({'status': 'error', 'message': 'All fields are required.'}), 400

        try:
            # Save the product details with both image paths
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO products (code, image, name, category, cost, price, current_stock) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (code, original_path, name, category, cost, price, current_stock)
            )
            conn.commit()
            conn.close()
            return jsonify({'status': 'success'}), 201
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Invalid file type'}), 400


@app.route('/update_product/<int:id>', methods=['PUT'])
def update_product(id):
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Define paths
            original_path = f'/static/uploads/product/original/{filename}'
            compress_path = f'/static/uploads/product/compress/{filename}'

            # Remove leading slash for actual file saving
            original_save_path = original_path[1:]
            compress_save_path = compress_path[1:]

            # Full paths
            original_full_path = os.path.join(os.getcwd(), original_save_path)
            compress_full_path = os.path.join(os.getcwd(), compress_save_path)

            # Ensure directories exist
            os.makedirs(os.path.dirname(original_full_path), exist_ok=True)
            os.makedirs(os.path.dirname(compress_full_path), exist_ok=True)

            # Save the original file
            file.save(original_full_path)

            # Open the image for resizing
            img = Image.open(file)

            # Resize the image to 30x30 for compression
            img = img.resize((30, 30))

            # Save the compressed image
            img.save(compress_full_path)

            image_path = original_path
    else:
        # If no new image is uploaded, keep the existing image
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT image FROM products WHERE id = ?', (id,))
        result = cursor.fetchone()
        conn.close()
        image_path = result['image'] if result else None

    # Get form data
    name = request.form.get('name')
    code = request.form.get('code')
    category = request.form.get('category')
    cost = request.form.get('cost')
    price = request.form.get('price')
    current_stock = request.form.get('current_stock')

    if not all([name, code]):
        return jsonify({'status': 'error', 'message': 'Name and Code are required.'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update the product in the database
        cursor.execute('''
            UPDATE products 
            SET name = ?, 
                code = ?, 
                image = ?, 
                category = ?, 
                cost = ?, 
                price = ?, 
                current_stock = ? 
            WHERE id = ?
        ''', (name, code, image_path, category, cost, price, current_stock, id))

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