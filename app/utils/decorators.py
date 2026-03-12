"""
Decoradores para autenticación y autorización
"""
from functools import wraps
from flask import session, redirect, url_for


def login_required(f):
    """Requiere que el usuario esté autenticado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Requiere que el usuario sea administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('auth.login'))
        if session.get('rol') != 'admin':
            return redirect(url_for('ordenes.index', error='acceso_denegado'))
        return f(*args, **kwargs)
    return decorated_function
