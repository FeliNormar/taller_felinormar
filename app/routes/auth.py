"""
Rutas de autenticación

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
from flask import Blueprint, render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash
from app.models.database import get_db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if session.get('logged_in'):
        return redirect(url_for('ordenes.index'))
    
    error = None
    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM usuarios WHERE usuario=?",
            (usuario,)
        ).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['logged_in'] = True
            session['usuario'] = user['usuario']
            session['rol'] = user['rol']
            return redirect(url_for('ordenes.index'))
        
        error = "Usuario o contraseña incorrectos."
    
    return render_template('login.html', error=error)


@auth_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    return redirect(url_for('auth.login'))
