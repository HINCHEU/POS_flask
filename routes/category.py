from flask import render_template, request, jsonify
from app import app
from routes.dashboard import get_db_connection
from routes.utils import role_required


@app.route('/admin/category')
@role_required('admin')
def category():  # put application's code here
    module = 'category'
    return render_template('admin/category.html', module=module)


# Get all categories
@app.route('/categories')
@role_required('admin')
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
@role_required('admin')
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
@role_required('admin')
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
@role_required('admin')
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
@role_required('admin')
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
