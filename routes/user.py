from flask import render_template, request, jsonify, session
from app import app
from routes.dashboard import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

from routes.utils import role_required


@app.route('/admin/user')
@role_required('admin')
def user_x():  # put application's code here
    module = 'user'
    return render_template('admin/user.html', module=module)


# -------------user----------
# Add new user
@app.route('/add_user', methods=['POST'])
@role_required('admin')
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
    password = data.get('password')

    hashed_password = generate_password_hash(password)

    if not all([code, name, email]):
        return jsonify({'status': 'error', 'message': 'Code, name, and email are required.'}), 400

    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO Users (code, profile, name, gender_id, role, email, phone, address,password) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)',
            (code, profile, name, gender_id, role, email, phone, address, hashed_password)
        )
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Update user
@app.route('/update_user/<int:id>', methods=['PUT'])
@role_required('admin')
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
@role_required('admin')
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
@role_required('admin')
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
@role_required('admin')
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


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE email = ?', (email,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['email'] = user['email']
        session['role'] = user['role']
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/login_admin')
def login_view():
    return render_template('admin/log_in.html')


@app.route('/logout')
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully!'}), 200
