from flask import render_template, request, jsonify
from app import app
from routes.dashboard import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from routes.utils import role_required


@app.route('/admin/sale')
@role_required('admin')
def sale():
    module = 'sale'
    return render_template('admin/sale.html', module=module)


@app.route('/get_sales', methods=['GET'])
@role_required('admin')
def get_sales():
    try:
        conn = get_db_connection()
        sales = conn.execute('SELECT * FROM sale').fetchall()
        conn.close()
        return jsonify([dict(sale) for sale in sales]), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/get_sale_detail/<int:sale_id>')
@role_required('admin')  # Ensure only admins can access this
def get_sale_detail(sale_id):
    try:
        conn = get_db_connection()

        # Fetch sale based on sale_id
        sale = conn.execute('SELECT * FROM sale WHERE id = ?', (sale_id,)).fetchone()
        print(sale)  # Debugging: print the fetched sale
        if not sale:
            return jsonify({'error': 'Sale not found'}), 404

        print(sale_id)  # Debugging: print the sale_id

        # Fetch related sale items using the sale_id parameter
        sale_items = conn.execute('SELECT * FROM sale_item WHERE sale_id = ?', (sale_id,)).fetchall()

        # Prepare items list
        items = []
        for item in sale_items:
            print(list(item.keys()))  # Debugging: print keys of the current item
            items.append({
                'quantity': item['quantity'],
                'price': item['price'],
                'subtotal': item['quantity'] * item['price']  # Calculate subtotal
            })

        conn.close()
        return jsonify({'items': items}), 200

    except Exception as e:
        # Log the error message for debugging
        print(f"Error fetching sale detail: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
