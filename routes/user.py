from flask import render_template, request, jsonify
from app import app
from routes.dashboard import get_db_connection


@app.route('/admin/user')
def user_x():  # put application's code here
    module = 'user'
    return render_template('admin/user.html', module=module)


# -------------user----------
# Add new user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    code = data.get('code')
    profile = data.get('profile')
    name = data.get('name')
    gender_id = data.get('gender_id')
    role = data.get('role')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')

    if not all([code, name, email]):
        return jsonify({'status': 'error', 'message': 'Code, name, and email are required.'}), 400

    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO Users (code, profile, name, gender_id, role, email, phone, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (code, profile, name, gender_id, role, email, phone, address)
        )
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Update user
@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    code = data.get('code')
    profile = data.get('profile')
    name = data.get('name')
    gender_id = data.get('gender_id')
    role = data.get('role')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')

    if not all([code, name, email]):
        return jsonify({'status': 'error', 'message': 'Code, name, and email are required.'}), 400

    try:
        conn = get_db_connection()
        conn.execute(
            'UPDATE Users SET code = ?, profile = ?, name = ?, gender_id = ?, role = ?, email = ?, phone = ?, address = ? WHERE id = ?',
            (code, profile, name, gender_id, role, email, phone, address, id)
        )
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Delete user
@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM Users WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM Users').fetchall()
        conn.close()
        return jsonify([dict(user) for user in users]), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Get user by ID
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    try:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE id = ?', (id,)).fetchone()
        conn.close()
        if user:
            return jsonify(dict(user)), 200
        else:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
