import os
from datetime import date, datetime
import requests
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
            'SELECT products.id,products.Code,products.current_stock,'
            'products.name,products.Cost,products.price,products.image,'
            'products.category AS category_id,'
            'categories.name AS category_name '
            'FROM products INNER JOIN categories'
            ' on products.category = categories.id;').fetchall()
        conn.close()

        product_list = [
            {
                'id': product['id'],
                'code': product['code'],
                # Update image path to point to the compressed image folder
                'image': f'/static/uploads/product/original/{product["image"].split("/")[-1]}',
                'name': product['name'],
                'category': product['category_name'],
                'category_id': product['category_id'],
                'cost': product['cost'],
                'price': product['price'],
                'current_stock': product['current_stock']
            } for product in products
        ]

        return jsonify(product_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/send-receipt-telegram', methods=['POST'])
def save_print():
    data = request.get_json()
    cart = data.get('carts')
    name = 'អតិថិជនធម្មតា'
    phone = 'None'
    bot_token = '6490003594:AAHGad1MucESpYtWXfUXDjcvGi-RucdmzaE'
    chat_id = '843851538'

    customer_details = (
        f"📅 <b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"✉️ <b>Receipt:</b> {'12345'}\n"
        f"👤 <b>Customer:</b>\n"
        f"    • <b>Name:</b> {name}\n"
        f"    • <b>Phone:</b> {phone}\n"
        f"____________________________\n"
        f"🛒 <b>Ordered Products:</b>\n"
    )
    full_message = customer_details
    total_cost = 0

    for index, product in enumerate(cart, start=1):
        product_id = product['id']
        product_name = product['name']
        price = product['price']
        quantity = product['quantity']
        item_total = price * quantity
        total_cost += item_total

        product_details = (
            f"  {index}. <b>{product_name}</b>\n"
            f"      • <b>Product ID:</b> {product_id}\n"
            f"      • <b>Price:</b> ${price:.2f}\n"
            f"      • <b>Quantity:</b> {quantity}\n"
            f"      • <b>Subtotal:</b> ${(quantity * price):.2f}\n"
        )
        full_message += product_details
    full_message += f"____________________________" \
                    f"\n💰 <b>Total Cost:</b> ${total_cost:.2f}\n"
    data = {
        'chat_id': chat_id,
        'text': full_message,
        'parse_mode': 'HTML'
    }

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    res = requests.post(url, data=data)
    print(res.json())

    return jsonify({'status': 'success'}), 201
