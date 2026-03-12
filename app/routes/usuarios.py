"""
Rutas para gestión de usuarios (solo admin)

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
from flask import Blueprint, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash
from app.models.database import get_db
from app.utils.decorators import admin_required

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@usuarios_bp.route('/')
@admin_required
def index():
    """Lista de usuarios"""
    conn = get_db()
    lista = conn.execute(
        "SELECT id, usuario, rol FROM usuarios ORDER BY id"
    ).fetchall()
    
    return render_template(
        'usuarios.html',
        usuarios=lista,
        usuario=session['usuario'],
        rol=session['rol']
    )


@usuarios_bp.route('/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_usuario():
    """Crear nuevo usuario"""
    error = None
    
    if request.method == 'POST':
        usu = request.form['usuario'].strip()
        pwd = request.form['password']
        rol = request.form.get('rol', 'tecnico')
        
        try:
            conn = get_db()
            conn.execute(
                "INSERT INTO usuarios (usuario, password, rol) VALUES (?,?,?)",
                (usu, generate_password_hash(pwd), rol)
            )
            conn.commit()
            return redirect(url_for('usuarios.index'))
        except Exception:
            error = "El nombre de usuario ya existe."
    
    return render_template(
        'nuevo_usuario.html',
        error=error,
        usuario=session['usuario'],
        rol=session['rol']
    )


@usuarios_bp.route('/eliminar/<int:uid>', methods=['POST'])
@admin_required
def eliminar_usuario(uid):
    """Eliminar un usuario"""
    conn = get_db()
    conn.execute(
        "DELETE FROM usuarios WHERE id=? AND usuario != 'admin'",
        (uid,)
    )
    conn.commit()
    return redirect(url_for('usuarios.index'))
