import os
from datetime import date, datetime
import requests
from flask import render_template, request, jsonify
from app import app
from routes.dashboard import get_db_connection
from routes.utils import login_required
from routes.product import get_products
from functools import wraps


@app.route('/sell')
@login_required
def sell():
    return render_template('user/index.html')


@app.route('/pos_products')
@login_required
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


@app.route('/get_last_sale_id')
@login_required
def get_last_sale_id():
    conn = get_db_connection()
    try:
        # Fetch the last ref_code from the `sale` table
        cursor = conn.cursor()
        cursor.execute("SELECT ref_code FROM sale ORDER BY id DESC LIMIT 1")
        last_ref_code = cursor.fetchone()

        if last_ref_code:
            last_ref_code = last_ref_code['ref_code']
            prefix, number = last_ref_code.rsplit('_', 1)
            new_number = str(int(number) + 1).zfill(3)
            last_ref_code = f"{prefix}_{new_number}"
    finally:
        conn.close()
    print(last_ref_code)
    return jsonify(last_ref_code), 200


@app.route('/payment', methods=['POST'])
@login_required
def save_print():
    data = request.get_json()
    cart = data.get('carts', [])
    order_date = data.get('timestamp')

    if not cart:
        return jsonify({'status': 'error', 'message': 'Cart is empty'}), 400

    conn = get_db_connection()
    try:
        # Fetch the last ref_code from the `sale` table
        cursor = conn.cursor()
        cursor.execute("SELECT ref_code FROM sale ORDER BY id DESC LIMIT 1")
        last_ref_code = cursor.fetchone()

        # Generate new ref_code
        if last_ref_code:
            last_ref_code = last_ref_code['ref_code']
            prefix, number = last_ref_code.rsplit('_', 1)
            new_number = str(int(number) + 1).zfill(3)
            ref_code = f"{prefix}_{new_number}"
        else:
            ref_code = "ref_code_001"  # Default ref_code if no records exist

        total_cost = sum(item['price'] * item['quantity'] for item in cart)

        # Insert into `sale` table
        cursor.execute("""
            INSERT INTO sale (ref_code, sale_date, total_amount, received_amount, status)
            VALUES (?, ?, ?, ?, ?)
        """, (ref_code, order_date, total_cost, total_cost, 1))

        # Fetch last inserted sale ID
        last_sale_id = cursor.lastrowid

        # Insert into `sale_item` table
        for product in cart:
            product_id = product['id']
            quantity = product['quantity']
            price = product['price']
            item_total = price * quantity

            cursor.execute("""
                INSERT INTO sale_item (sale_id, product_id, quantity, price, total)
                VALUES (?, ?, ?, ?, ?)
            """, (last_sale_id, product_id, quantity, price, item_total))

        conn.commit()  # Commit the transaction

    except Exception as e:
        conn.rollback()  # Rollback in case of error
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()  # Ensure the connection is closed

    # Telegram Notification (unchanged)
    name = 'អតិថិជនធម្មតា'
    phone = 'None'
    bot_token = '6490003594:AAHGad1MucESpYtWXfUXDjcvGi-RucdmzaE'
    chat_id = '843851538'

    customer_details = (
        f"📅 <b>Date:</b> {order_date}\n"
        f"✉️ <b>Receipt:</b> {ref_code}\n"
        f"👤 <b>Customer:</b>\n"
        f"    • <b>Name:</b> {name}\n"
        f"    • <b>Phone:</b> {phone}\n"
        f"____________________________\n"
        f"🛒 <b>Ordered Products:</b>\n"
    )

    full_message = customer_details

    for index, product in enumerate(cart, start=1):
        product_name = product['name']
        price = product['price']
        quantity = product['quantity']
        item_total = price * quantity

        product_details = (
            f"  {index}. <b>{product_name}</b>\n"
            f"      • <b>Product ID:</b> {product['id']}\n"
            f"      • <b>Price:</b> ${price:.2f}\n"
            f"      • <b>Quantity:</b> {quantity}\n"
            f"      • <b>Subtotal:</b> ${(item_total):.2f}\n"
        )
        full_message += product_details

    full_message += f"____________________________" \
                    f"\n💰 <b>Total Cost:</b> ${total_cost:.2f}\n"

    # Send message to Telegram
    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data={
        'chat_id': chat_id,
        'text': full_message,
        'parse_mode': 'HTML'
    })

    return jsonify({'status': 'success'}), 201
