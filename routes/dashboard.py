from flask import render_template, request, jsonify, redirect, session, url_for
from app import app
import sqlite3
from werkzeug.utils import secure_filename
import os
from PIL import Image
from functools import wraps

from routes.utils import role_required

app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/admin')
@app.route('/')
@role_required('admin')
def dashboard():  # put application's code here
    module = 'dashboard'
    return render_template('admin/dashboard.html', module=module)


@app.route('/user')
@role_required('admin')
def user():  # put application's code here
    module = 'user'
    return render_template('admin/user.html', module=module)


@app.route('/admin/table')
@role_required('admin')
def table():  # put application's code here
    module = 'table'
    return render_template('admin/table.html', module=module)


@app.route('/admin/profile')
@role_required('admin')
def profile():  # put application's code here
    module = 'profile'
    return render_template('admin/profile.html', module=module)


@app.route('/admin/billing')
@role_required('admin')
def billing():  # put application's code here
    module = 'billing'
    return render_template('admin/billing.html', module=module)
