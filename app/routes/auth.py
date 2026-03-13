"""
Rutas de autenticación

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import check_password_hash
from app.models.database import get_db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Página de inicio de sesión
    
    Implementa limpieza de sesión antes de cada login para evitar
    conflictos con el middleware de verificación.
    """
    # Si ya está logueado, redirigir al dashboard
    if session.get('logged_in'):
        return redirect(url_for('ordenes.index'))
    
    if request.method == 'POST':
        # Limpiar sesión antes de procesar login (seguridad)
        session.clear()
        
        usuario = request.form.get('usuario', '').strip()
        password = request.form.get('password', '')
        
        # Validaciones
        if not usuario or not password:
            flash('Usuario y contraseña son obligatorios', 'error')
            return render_template('login.html')
        
        try:
            conn = get_db()
            user = conn.execute(
                "SELECT * FROM usuarios WHERE usuario=?",
                (usuario,)
            ).fetchone()
            
            if user and check_password_hash(user['password'], password):
                # Login exitoso - establecer sesión
                session.clear()  # Limpiar cualquier dato residual
                session['logged_in'] = True
                session['usuario'] = user['usuario']
                session['rol'] = user['rol']
                session.permanent = True  # Hacer la sesión permanente
                
                flash(f'Bienvenido, {user["usuario"]}!', 'success')
                return redirect(url_for('ordenes.index'))
            else:
                flash('Usuario o contraseña incorrectos', 'error')
                
        except Exception as e:
            flash(f'Error al iniciar sesión: {str(e)}', 'error')
    
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """
    Cerrar sesión
    
    Limpia completamente la sesión y redirige al login.
    """
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('auth.login'))
