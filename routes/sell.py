from flask import render_template, request, jsonify
from app import app
from routes.dashboard import get_db_connection
from routes.product import get_products


@app.route('/sell')
def sell():
    return render_template('user/index.html')


@app.route('/pos_products')
def get_products_pos():
    try:
        conn = get_db_connection()
        products = conn.execute(
            'SELECT products.id,products.Code,products.current_stock,products.name,products.Cost,products.price,products.image,categories.name AS category_name FROM products INNER JOIN categories on products.category = categories.id;').fetchall()
        conn.close()

        product_list = [
            {
                'id': product['id'],
                'code': product['code'],
                # Update image path to point to the compressed image folder
                'image': f'/static/uploads/product/original/{product["image"].split("/")[-1]}',
                'name': product['name'],
                'category': product['category_name'],
                'cost': product['cost'],
                'price': product['price'],
                'current_stock': product['current_stock']
            } for product in products
        ]

        return jsonify(product_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
