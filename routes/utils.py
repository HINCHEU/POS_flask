from functools import wraps
from flask import session, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_view'))
        return f(*args, **kwargs)

    return decorated_function


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('login_view'))  # Redirect to login page if unauthorized
            return f(*args, **kwargs)

        return decorated_function

    return decorator
